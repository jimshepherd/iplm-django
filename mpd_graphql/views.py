import xlsxwriter.utility
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render

import json
import xlsxwriter as write_xl
from xlsxwriter.utility import xl_range, xl_rowcol_to_cell
from mpd_graphql.models import ProcessMethod

# Create your views here.


def create_test(request):
    """ A view that creates and downloads a Test from a Test Plan """
    test_plan_id = request.GET.get('id')
    test_name = request.GET.get('name')
    test_lot = request.GET.get('lot')
    cavities = request.GET.get('cavities')

    print('test_plan_id', test_plan_id)
    print('test_name', test_name)
    print('test_lot', test_lot)
    print('cavities', cavities)
    cavities = [cavity.strip() for cavity in cavities.split(',')]

    num_cavities = len(cavities)
    print('num_cavities', num_cavities)

    test_plan = ProcessMethod.objects.get(pk=test_plan_id)

    file_name = f'Test {test_name}.xlsx'

    workbook = write_xl.Workbook(file_name)

    heading_format = workbook.add_format({'bold': True, 'bg_color': '#002060', 'font_color': 'white'})
    entry_format = workbook.add_format({'bg_color': 'white'})
    unused_format = workbook.add_format({'bg_color': '#A6A6A6'})
    out_of_control_format = workbook.add_format({'bg_color': '#FFC000'})
    out_of_spec_format = workbook.add_format({'bg_color': 'red'})
    not_plausible_format = workbook.add_format({'bg_color': 'black',  'font_color': 'white'})

    acceptable_format = workbook.add_format({'bg_color': '#FFE699'})
    target_format = workbook.add_format({'bg_color': 'white'})
    marginal_format = workbook.add_format({'bg_color': '#FFCC66'})
    unacceptable_format = workbook.add_format({'bg_color': 'red'})

    sheet = workbook.add_worksheet(name='Test')
    sheet.set_column(0, 1, 12)

    print(f'Test {test_name} being exported')
    row = 0
    sheet.write(row, 0, 'Test', heading_format)
    sheet.write_blank(row, 1, None, heading_format)
    row += 1
    sheet.write_blank(row, 0, None, heading_format)
    sheet.write(row, 1, 'Name', heading_format)
    sheet.write(row, 2, test_name)
    row += 1
    sheet.write_blank(row, 0, None, heading_format)
    sheet.write(row, 1, 'Id', heading_format)
    sheet.write(row, 2, int(test_plan.id))
    row += 1
    sheet.write_blank(row, 0, None, heading_format)
    sheet.write(row, 1, 'Description', heading_format)
    sheet.write(row, 2, test_plan.description)

    spec = test_plan.parent
    row += 1
    sheet.write(row, 0, 'Master Specification', heading_format)
    sheet.write_blank(row, 1, None, heading_format)
    row += 1
    sheet.write_blank(row, 0, None, heading_format)
    sheet.write(row, 1, 'Id', heading_format)
    sheet.write(row, 2, int(spec.id))
    row += 1
    sheet.write_blank(row, 0, None, heading_format)
    sheet.write(row, 1, 'Name', heading_format)
    sheet.write(row, 2, spec.name)

    product = test_plan.material_specifications_in.first()
    row += 1
    sheet.write(row, 0, 'Product', heading_format)
    sheet.write_blank(row, 1, None, heading_format)
    row += 1
    sheet.write_blank(row, 0, None, heading_format)
    sheet.write(row, 1, 'Id', heading_format)
    sheet.write(row, 2, int(product.id))
    row += 1
    sheet.write_blank(row, 0, None, heading_format)
    sheet.write(row, 1, 'Name', heading_format)
    sheet.write(row, 2, product.name)

    row += 1
    sheet.write_blank(row, 0, None, heading_format)
    sheet.write(row, 1, 'Lot', heading_format)
    sheet.write(row, 2, test_lot)
    row += 1
    sheet.write_blank(row, 0, None, heading_format)
    sheet.write(row, 1, 'Cavities', heading_format)
    sheet.write(row, 2, ', '.join(cavities))

    mic_fields = [
        'LPL',
        'LSL',
        'LCL',
        'Target',
        'UCL',
        'USL',
        'UPL',
        'Tolerance',
        'Test Method',
        'Format',
        'Calculation',
    ]

    sample_headings = ['Sample Type', 'Sample Size']
    mic_headings = ['Id', 'Name', 'Unit']

    row += 1
    mic_row = row + 1
    col = 0
    for mic_field in mic_headings + mic_fields + sample_headings:
        row += 1
        sheet.write(row, col, mic_field, heading_format)

    test_plans = test_plan.steps.all()

    max_num_measurements = 0
    max_mold_rounds = 0
    for step in test_plans:
        sample_type = step.properties.filter(property_type__name='Sample Type').first().text_value
        sample_size = step.properties.filter(property_type__name='Sample Size').first().int_value
        num_measurements = sample_size
        if sample_type == 'MR':
            num_measurements *= num_cavities
            max_mold_rounds = max(max_mold_rounds, sample_size)
        max_num_measurements = max(max_num_measurements, num_measurements)

    sample_row = row + 1

    row = sample_row + 1
    col = 0
    sheet.write(row, col, 'Samples', heading_format)
    for i in range(max_num_measurements):
        row += 1
        sheet.write(row, col, i + 1, heading_format)

    row += 2
    formula_row = row + 1
    for head in ['Min/Unacceptable', 'Average/Marginal', 'Max/Acceptable', 'Stdev/Target', 'CPK/Acceptable Rate']:
        row += 1
        sheet.write(row, col, head, heading_format)

    row = sample_row + 1
    col = 1
    sheet.write(row, col, 'Cavities', heading_format)
    for i in range(max_mold_rounds):
        for cavity in cavities:
            row += 1
            sheet.write(row, col, cavity, heading_format)

    field_rows = dict()
    col += 1
    for step in test_plans:
        mic = step.property_specs.first()
        row = mic_row
        col += 1
        sheet.write(row, col, int(mic.id), heading_format)
        row += 1
        sheet.write(row, col, mic.name, heading_format)
        row += 1
        sheet.write(row, col, mic.unit, heading_format)

        values = mic.values
        for i, mic_field in enumerate(mic_fields):
            try:
                value = values[mic_field]
            except KeyError:
                value = ''
            row += 1
            sheet.write(row, col, value, heading_format)

            field_rows[mic_field] = row

        row += 1
        sample_type = step.properties.filter(property_type__name='Sample Type').first().text_value
        sheet.write(row, col, sample_type, heading_format)
        row += 1
        sample_size = step.properties.filter(property_type__name='Sample Size').first().int_value
        sheet.write(row, col, sample_size, heading_format)

        num_measurements = sample_size
        if sample_type == 'MR':
            num_measurements *= num_cavities

        # If Acceptable or Unacceptable, add conditional cells
        acceptable = []
        try:
            acceptable.extend(values['Acceptable'])
        except KeyError:
            pass
        try:
            acceptable.extend(values['Unacceptable'])
        except KeyError:
            pass
        row += 3
        data_range = xl_range(row, col, row + num_measurements - 1, col)
        if acceptable:
            sheet.data_validation(data_range, {
                'validate': 'list',
                'source': acceptable,
            })
        this_cell = xl_rowcol_to_cell(row, col)  # F50
        lpl_cell = xl_rowcol_to_cell(field_rows['LPL'], col, row_abs=True)  # F26
        lsl_cell = xl_rowcol_to_cell(field_rows['LSL'], col, row_abs=True)  # F27
        lcl_cell = xl_rowcol_to_cell(field_rows['LCL'], col, row_abs=True)  # F28
        target_cell = xl_rowcol_to_cell(field_rows['Target'], col, row_abs=True)  # F29
        ucl_cell = xl_rowcol_to_cell(field_rows['UCL'], col, row_abs=True)  # F30
        usl_cell = xl_rowcol_to_cell(field_rows['USL'], col, row_abs=True)  # F31
        upl_cell = xl_rowcol_to_cell(field_rows['UPL'], col, row_abs=True)  # F32
        calc_cell = xl_rowcol_to_cell(field_rows['Calculation'], col, row_abs=True)  # F44

        sheet.conditional_format(data_range, {
            'type': 'formula',
            'criteria': f'=ISBLANK({this_cell})',
            'format': unused_format,
            'stop_if_true': True,
        })

        # =OR(AND(F$44="Y",OR(F50="",F50=0)),$B50>F$48)
        # Use NOT ISBLANK since Calculation is a type not Y or blank
        # Condition only applied to active cells, so $B50>F$48 not needed (sample # > num samples)
        sheet.conditional_format(data_range, {
            'type': 'formula',
            'criteria': f'=AND(NOT(ISBLANK({calc_cell})),OR({this_cell}="",{this_cell}=0))',
            'format': unused_format,
            'stop_if_true': True,
        })

        # =AND(F$44="Y",OR(AND(F50>F$28,F50<F$29),AND(F50>F$28,F50<F$30),AND(F50>F$29,F50<F$30)))
        if all(limit in values for limit in ['LCL', 'Target', 'UCL']):
            sheet.conditional_format(data_range, {
                'type': 'formula',
                'criteria': f'=OR('
                            f'AND({this_cell}>{lcl_cell},{this_cell}<{target_cell}),'
                            f'AND({this_cell}>{lcl_cell},{this_cell}<{ucl_cell}),'
                            f'AND({this_cell}>{target_cell},{this_cell}<{ucl_cell}))',
                'format': unused_format,
                'stop_if_true': True,
            })

        # =AND(F$39="Y",OR(AND(F50>F$27,F50<F$28),AND(F50>F$30,F50<F$31),F50=F$27,F50=F$31))
        if all(limit in values for limit in ['LSL', 'LCL', 'UCL', 'USL']):
            sheet.conditional_format(data_range, {
                'type': 'formula',
                'criteria': f'=OR('
                            f'AND({this_cell}>{lsl_cell},{this_cell}<{lcl_cell}),'
                            f'AND({this_cell}>{ucl_cell},{this_cell}<{usl_cell}),'
                            f'{this_cell}={lsl_cell},'
                            f'{this_cell}={usl_cell})',
                'format': out_of_control_format,
                'stop_if_true': True,
            })

        # =AND(F$39="Y",OR(AND(F50>F$26,F50<F$27),AND(F50>F$31,F50<F$32)))
        if all(limit in values for limit in ['LPL', 'LSL', 'USL', 'UPL']):
            sheet.conditional_format(data_range, {
                'type': 'formula',
                'criteria': f'=OR('
                            f'AND({this_cell}>{lpl_cell},{this_cell}<{lsl_cell}),'
                            f'AND({this_cell}>{usl_cell},{this_cell}<{upl_cell}))',
                'format': out_of_spec_format,
                'stop_if_true': True,
            })

        # =AND(F$39="Y",OR(F50<F$27,F50>F$31))
        if all(limit in values for limit in ['LPL', 'UPL']):
            sheet.conditional_format(data_range, {
                'type': 'formula',
                'criteria': f'=OR('
                            f'{this_cell}<={lpl_cell},'
                            f'{this_cell}>={upl_cell})',
                'format': not_plausible_format,
                'stop_if_true': True,
            })

        if 'Unacceptable' in acceptable:
            sheet.conditional_format(data_range, {
                'type': 'cell',
                'criteria': '==',
                'value': 'Unacceptable',
                'format': unacceptable_format,
                'stop_if_true': True,
            })

        if 'Marginal' in acceptable:
            sheet.conditional_format(data_range, {
                'type': 'cell',
                'criteria': '==',
                'value': 'Marginal',
                'format': marginal_format,
                'stop_if_true': True,
            })

        if 'Acceptable' in acceptable:
            sheet.conditional_format(data_range, {
                'type': 'cell',
                'criteria': '==',
                'value': 'Acceptable',
                'format': acceptable_format,
                'stop_if_true': True,
            })

        if 'Target' in acceptable:
            sheet.conditional_format(data_range, {
                'type': 'cell',
                'criteria': '==',
                'value': 'Target',
                'format': target_format,
                'stop_if_true': True,
            })

        #for i in range(num_measurements):
        #    sheet.write_blank(row, col, None, entry_format)
        #    row += 1
        print('formula rows', row + num_measurements - 1, row + max_num_measurements)
        for i in range(row + num_measurements - 1, row + max_num_measurements):
            sheet.write_blank(row, col, None, unused_format)
            row += 1

        row = formula_row
        if acceptable:
            sheet.write_formula(row, col, f'=COUNTIF({data_range}, "=Unacceptable")')
        else:
            sheet.write_formula(row, col, f'=MIN({data_range})')

        row += 1
        if acceptable:
            sheet.write_formula(row, col, f'=COUNTIF({data_range}, "=Marginal")')
        else:
            sheet.write_formula(row, col, f'=AVERAGE({data_range})')

        row += 1
        if acceptable:
            sheet.write_formula(row, col, f'=COUNTIF({data_range}, "=Acceptable")')
        else:
            sheet.write_formula(row, col, f'=MAX({data_range})')

        row += 1
        if acceptable:
            sheet.write_formula(row, col, f'=COUNTIF({data_range}, "=Target")')
        else:
            sheet.write_formula(row, col, f'=STDEV({data_range})')

        # =MIN(F$31-F$92,F$92-F$27)/(3*F$94)
        row += 1
        if acceptable:
            sheet.write_formula(row, col, f'=COUNTIF({data_range}, "=Marginal")'
                                          f'+COUNTIF({data_range}, "=Acceptable")'
                                          f'+COUNTIF({data_range}, "=Target")')
        else:
            sheet.write_formula(row, col, f'=MIN('
                                          f'{usl_cell}-AVERAGE({data_range}),'
                                          f'AVERAGE({data_range})-{lsl_cell})'
                                          f'/(3*STDEV({data_range}))')

    workbook.close()

    response = HttpResponse(
        open(file_name, 'rb'),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename='+f'Test_{test_name}.xlsx'
    return response
