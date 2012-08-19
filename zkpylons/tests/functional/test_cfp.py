import md5
import re

from paste.fixture import Dummy_smtplib

from zkpylons.model import Person, Proposal, ProposalType, Attachment
from zkpylons.tests.functional import *


#class TestCFPController(ControllerTest):

# TODO
# * test the different states work by setting them somehow

#    def __init__(self, *args):
#        self.cfp_status = None
#        super(TestCFPController, self).__init__(*args)
#
#    def setUp(self):
#        #self.cfp_status = environ['paste.config']['app_conf']['cfp_status']
#        print "Moo"
#        print self.app.app.global_conf
#        print "Cow"
#
#    def tearDown(self):
#        #environ['paste.config']['app_conf']['cfp_status'] = self.cfp_status
#        pass
#
#    def test_index(self):
#        res = self.app.get('/cfp')
#        raise
#
#    def test_index_module_not_open(self):
#        #request.environ['paste.config']['app_conf'].set('cfp_status', 'not_open')
#        resp = self.app.get('/cfp')
#        resp.mustcontain("is not open!")
#
#    def test_index_module_open(self):
#        #        request.environ['paste.config']['app_conf'].set('cfp_status', 'open')
#        resp = self.app.get('/cfp')
#        resp.mustcontain("is open!")
#
#    def test_index_module_closed(self):
#        #        request.environ['paste.config']['app_conf'].set('cfp_status', 'closed')
#        resp = self.app.get('/cfp')
#        resp.mustcontain("is closed!")

#class TestCFP(CRUDControllerTest):
#    def test_index(self):
#        res = self.app.get('/cfp')
        
#     def test_create(self):
#         response = self.app.get('/cfp/submit')
#         form = response.form

#         print form.text
#         print form.fields

#         reg_data = {'email_address': 'testguy@example.org',
#                     'password': 'password',
#                     'password_confirm': 'password',
#                    }
#         sub_data = {'title': 'title',
#                     'abstract': 'abstract',
#                     'type': 1,
#                     'experience': 'some',
#                     'url': 'http://example.org',
#                     'assistance': True,
#                     }
#         for k in reg_data.keys():
#             form['registration.' + k] = reg_data[k]
#         for k in sub_data.keys():
#             form['proposal.' + k] = sub_data[k]
#         form['attachment'] = "foo"

#         form.submit()

#         regs = self.dbsession.query(Person).select()
#         self.assertEqual(1, len(regs))

#         for key in reg_data.keys():
#             self.check_attribute(regs[0], key, reg_data[key])

#         subs = self.dbsession.query(Proposal).select()
#         self.assertEqual(1, len(subs))

#         for key in sub_data.keys():
#             self.check_attribute(subs[0], key, sub_data[key])

#         atts = self.dbsession.query(Attachment).select()
#         self.assertEqual(1, len(atts))
#         self.assertEqual('foo', str(atts[0].content))
                         

#         self.dbsession.delete(regs[0])
#         self.dbsession.delete(subs[0])
#         self.dbsession.flush()

#     # FIXME: not testing type
#     no_test = ['password_confirm', 'type']
#     mangles = dict(password = lambda p: md5.new(p).hexdigest(),
#                    attachment = lambda a: buffer(a),
#                    #type = lambda t: TestCFP.self.dbsession.query(ProposalType).get(1),
#                    )

#     def setUp(self):
#         super(TestCFP, self).setUp()
#         st1 = ProposalType('Paper')
#         st2 = ProposalType('Scissors')
#         self.dbsession.save(st1)
#         self.dbsession.save(st2)
#         self.dbsession.flush()
#         self.stid = (st1.id, st2.id)

#     def tearDown(self):
#         st1 = self.dbsession.query(ProposalType).get(self.stid[0])
#         st2 = self.dbsession.query(ProposalType).get(self.stid[1])
#         self.dbsession.delete(st2)
#         self.dbsession.delete(st1)
#         self.dbsession.flush()

#         super(TestCFP, self).tearDown()


#     def test_cfp_registration(self):
#         # set up the smtp catcher
#         Dummy_smtplib.install()
        
#         # submit to the cfp
#         res = self.app.get('/cfp/submit')
#         form = res.form
#         d = {'registration.email_address': 'testguy@example.org',
#              'registration.password': 'test',
#              'registration.password_confirm': 'test',
#              'registration.fullname': 'Testguy McTest',
#              'proposal.title': 'title',
#              'proposal.abstract': 'abstract',
#              'proposal.type': 1,
#              'proposal.assistance': False,
#              'attachment': 'foo'
#              }
#         for k in d.keys():
#             form[k] = d[k]
#         res1 = form.submit()

#         # thankyou page says what email address got sent to
#         res1.mustcontain('testguy@example.org')

#         # grab it from the db
#         regs = self.dbsession.query(Person).select()
#         self.assertEqual(1, len(regs))
#         # make sure that it's inactive
#         self.assertEqual(False, regs[0].activated)

#         # clear this session, we want to reselect this data later
#         self.dbsession.clear()
        
        
#         # get out the url hash because i don't know how to trap smtplib
#         self.failIfEqual(None, Dummy_smtplib.existing, "no message sent from proposal")
        
#         message = Dummy_smtplib.existing

#         print "message: '''%s'''" % message.message

#         # check that the message goes to the right place
#         self.assertEqual("testguy@example.org", message.to_addresses)

#         # check that the message has the to address in it
#         to_match = re.match(r'^.*To:.*testguy@example.org.*', message.message, re.DOTALL)
#         self.failIfEqual(None, to_match, "to address not in headers")

#         # check that the message has the submitter's name
#         name_match = re.match(r'^.*Testguy McTest', message.message, re.DOTALL)
#         self.failIfEqual(None, name_match, "submitter's name not in headers")

#         # check that the message was renderered without HTML, i.e.
#         # as a fragment and thus no autohandler crap
#         html_match = re.match(r'^.*<!DOCTYPE', message.message, re.DOTALL)
#         self.failUnlessEqual(None, html_match, "HTML in message!")
        
#         # check that the message has a url hash in it
#         match = re.match(r'^.*/person/confirm/(\S+)', message.message, re.DOTALL)
#         print "match:", match
#         self.failIfEqual(None, match, "url not found")

#         # visit the url
#         print "match: '''%s'''" % match.group(1)
#         res = self.app.get('/person/confirm/%s' % match.group(1))
#         print res
        
#         # check the rego worked
#         regs = self.dbsession.query(Person).select()
#         self.assertEqual(1, len(regs))
#         print regs[0]
#         self.assertEqual(True, regs[0].activated, "account was not activated!")

#         # clean up
#         Dummy_smtplib.existing.reset()

#         self.dbsession.delete(regs[0])
#         self.dbsession.delete(self.dbsession.query(Proposal).select()[0])
#         self.dbsession.flush()

#         self.assertEmptyModel(Proposal)
#         self.assertEmptyModel(Person)
#         self.assertEmptyModel(Attachment)
