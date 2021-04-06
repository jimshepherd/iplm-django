from mixer.backend.django import mixer

from mpd_graphql.models import Address, Organization, OrganizationType

from .mpd_graphql import MPDGraphQLTestCase


ORGANIZATIONS_QUERY = '''
query organizations {
    organizations {
        id
        name
        description
        orgTypes {
            id
            name
        }
        addresses {
            id
            street
            street2
            city
            state
            country
            zip
        }
    }
}
'''

ORGANIZATION_TYPES_QUERY = '''
query organizationTypes {
    organizationTypes {
        id
        name
        description
    }
}
'''

UPDATE_ORGANIZATION_MUTATION = '''
mutation updateOrganization($organization: OrganizationInput!) {
    updateOrganization(organization: $organization) {
        organization {
            id
            name
            description
            orgTypes {
                id
                name
            }
            addresses {
                id
                street
                street2
                city
                state
                country
                zip
            }
        }
    }
}
'''

UPDATE_ORGANIZATION_TYPE_MUTATION = '''
mutation updateOrganizationType($organizationType: OrganizationTypeInput!) {
    updateOrganizationType(organizationType: $organizationType) {
        organizationType {
            id
            name
            description
        }
    }
}
'''


class OrganizationUnitTestCase(MPDGraphQLTestCase):

    def setUp(self):
        super().setUp()
        self.org_type1 = mixer.blend(OrganizationType)
        self.org_type2 = mixer.blend(OrganizationType)
        #with mixer.ctx(commit=False):
        #    self.address1 = mixer.blend(Address)
        #    self.address2 = mixer.blend(Address)
        self.org1 = mixer.blend(Organization,
                                org_types=[self.org_type1])
        self.address1 = mixer.blend(Address, organization=self.org1)
        # self.org1.addresses.set([self.address1])
        self.org2 = mixer.blend(Organization,
                                org_types=[self.org_type2, self.org_type2])
        # self.org2.addresses.set([self.address2])
        self.address2 = mixer.blend(Address, organization=self.org2)

    def test_organizations(self):

        response = self.client.execute(ORGANIZATIONS_QUERY, {})
        # print('test_organizations response', response)
        data = response.data
        # print('test_organizations data', data)

        assert len(data['organizations']) == 2

    def test_organization_types(self):

        response = self.client.execute(ORGANIZATION_TYPES_QUERY, {})
        data = response.data
        # print('test_organization_types data', data)

        assert len(data['organizationTypes']) == 2

    def test_update_organization(self):

        name = 'Updated name'
        description = 'Updated description'
        street = 'Updated street'
        street2 = 'Updated street2'
        city = 'Updated city'
        state = 'Updated state'
        country = 'Updated country'
        zip = 'Updated zip'
        variables = {
            'organization': {
                'id': self.org1.id,
                'name': name,
                'description': description,
                'orgTypes': [
                    {
                        'id': self.org_type2.id,
                    },
                ],
                'addresses': [
                    {
                        'id': self.address1.id,
                        'street': street,
                        'street2': street2,
                        'city': city,
                        'state': state,
                        'country': country,
                        'zip': zip,
                    }
                ],
            }
        }
        response = self.client.execute(UPDATE_ORGANIZATION_MUTATION, variables)
        # print('test_update_organization response', response)
        data = response.data
        # print('test_update_organization data', data)

        org = data['updateOrganization']['organization']
        self.assertEqual(org['name'], name)
        self.assertEqual(org['description'], description)
        self.assertEqual(len(org['orgTypes']), 1)
        org_type = org['orgTypes'][0]
        self.assertEqual(int(org_type['id']), self.org_type2.id)
        self.assertEqual(len(org['addresses']), 1)
        address = org['addresses'][0]
        self.assertEqual(address['street'], street)
        self.assertEqual(address['street2'], street2)
        self.assertEqual(address['city'], city)
        self.assertEqual(address['state'], state)
        self.assertEqual(address['country'], country)
        self.assertEqual(address['zip'], zip)

        # Make sure the update did not create a new address
        addresses = Address.objects.all()
        self.assertEqual(len(addresses), 2)

    def test_update_organization_type(self):

        name = 'Updated Name'
        description = 'Updated description'
        variables = {
            'organizationType': {
                'id': self.org_type1.id,
                'name': name,
                'description': description,
            }
        }
        response = self.client.execute(UPDATE_ORGANIZATION_TYPE_MUTATION, variables)
        data = response.data
        # print('test_update_organization_type data', data)

        org_type = data['updateOrganizationType']['organizationType']
        self.assertEqual(org_type['name'], name)
        self.assertEqual(org_type['description'], description)
