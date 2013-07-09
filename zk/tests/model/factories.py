"""
zk/model/attachment.py          zk/model/meta.py                         zk/model/rego_note.py
zk/model/ceiling.py             zk/model/password_reset_confirmation.py  zk/model/rego_room.py
zk/model/contentstor.py         zk/model/payment_allocation.py           zk/model/review.py
zk/model/db_content.py          zk/model/payment.py                      zk/model/role.py
zk/model/event.py               zk/model/payment_received.py             zk/model/schedule.py
zk/model/event_type.py          zk/model/person_proposal_map.py          zk/model/social_network.py
zk/model/forms.py               zk/model/person.py                       zk/model/special_offer.py
zk/model/fulfilment.py          zk/model/person_role_map.py              zk/model/special_registration.py
zk/model/funding_attachment.py  zk/model/person_social_network_map.py    zk/model/stream.py
zk/model/funding.py             zk/model/product_category.py             zk/model/time_slot.py
zk/model/funding_review.py      zk/model/product_ceiling_map.py          zk/model/travel.py
zk/model/__init__.py            zk/model/product.py                      zk/model/url_hash.py
zk/model/invoice_item.py        zk/model/proposal.py                     zk/model/volunteer.py
zk/model/invoice.py             zk/model/registration_product.py         zk/model/vote.py
zk/model/location.py            zk/model/registration.py                 zk/model/voucher.py
"""

import datetime
from sqlalchemy import Column, Integer, Unicode, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from zk.model.meta import Base
from zk.model.person import Person
import factory
from factory.alchemy import SQLAlchemyModelFactory


session = scoped_session(sessionmaker())
engine = create_engine('sqlite://')
session.configure(bind=engine)
Base.metadata.create_all(engine)


class PersonFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = Person
    FACTORY_SESSION = session   # the SQLAlchemy session object

    id = factory.Sequence(lambda n: n)
    email_address = factory.LazyAttribute(lambda obj: '{}@example.com'.format(obj.fullname.replace(' ', '')))
    password = "password"
    creation_timestamp = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    last_modification_timestamp = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())  
    firstname = factory.Sequence(lambda n: u'User %d' % n)
    lastname = "Doe"
    fullname = factory.LazyAttribute(lambda obj: '{} {}'.format(obj.firstname, obj.lastname))
    address1 = factory.Sequence(lambda n: u'%d Main Street' % n)
    city = factory.Sequence(lambda n: u'Suburb %d' % n)
    state = 'VIC'
    postcode = '3000'
    country = 'Australia'
    mobile = factory.Sequence(lambda n: '04%08d' % n)
    url = factory.LazyAttribute(lambda obj: 'http://www.{}.com'.format(obj.fullname.replace(' ', ''))) 

