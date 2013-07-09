from factories import PersonFactory


def test_factory_basics():
    '''Testing the defaults that we set with factory_boy
    '''
    a = PersonFactory()
    assert a.firstname == "User 1"
    assert a.lastname == "Doe"
    assert a.fullname == "User 1 Doe"
    assert a.email_address == "User1Doe@example.com"
    assert repr(a) == '<Person id="1" email="User1Doe@example.com">'
    assert a.address1 == '1 Main Street'
    assert a.address2 == None
    assert a.city == 'Suburb 1'
    assert a.state == 'VIC'
    assert a.postcode == '3000'
    assert a.country == 'Australia'
    assert a.mobile == '0400000001'
    assert a.url == 'http://www.User1Doe.com'


def test_password_hashing():
    '''We are not storing passwords as plaintext, hooray
    '''
    a = PersonFactory(password='python')
    assert a.check_password('python')
    assert a.password != 'python'
    assert a.password_hash != 'python'


def test_default_roles():
    a = PersonFactory()
    assert a.roles == []
    assert not a.is_speaker()
    assert not a.is_miniconf_org()
    assert not a.is_professional()
    assert not a.is_volunteer()


def test_is_from_common_country():
    a = PersonFactory(country='Australia')
    assert a.is_from_common_country()
    b = PersonFactory(country='Venezuela')
    assert not b.is_from_common_country()


"""
    assert not a.has_valid_invoice()
    assert not a.has_paid_ticket()
has_role
valid_invoice
ticket_type
paid
fetch_social_networks
avatar_url
find_review_summary

class methods
-------------
find_by_email
find_by_id
find_all
find_by_url_hash
"""
