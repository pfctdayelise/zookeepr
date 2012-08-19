import datetime

from zkpylons.tests.model import *

class TestProposal(CRUDModelTest):
        
    def test_create(self):
        self.domain = model.proposal.Proposal

        self.check_empty_session()

        st = model.ProposalType(name='BOF')

        # create a person to submit with
        v = model.Person('hacker', 'hacker@example.org',
                   'p4ssw0rd',
                   'E.',
                   'Leet',
                   '+6125555555',
                   )

        print v

        self.dbsession.save(st)
        self.dbsession.save(v)
        self.dbsession.flush()

        s = model.Proposal(title='Venal Versimilitude: Vast vocation or violition of volition?',
                       type=st,
                       abstract='This visage, no mere veneer of vanity, is it vestige of the vox populi, now vacant, vanished, as the once vital voice of the verisimilitude now venerates what they once vilified. However, this valorous visitation of a by-gone vexation, stands vivified, and has vowed to vanquish these venal and virulent vermin vanguarding vice and vouchsafing the violently vicious and voracious violation of volition. The only verdict is vengeance; a vendetta, held as a votive, not in vain, for the value and veracity of such shall one day vindicate the vigilant and the virtuous. Verily, this vichyssoise of verbiage veers most verbose vis-a-vis an introduction, and so it is my very good honor to meet you and you may call me V.',
                       )
        
        # give this sub to v
        v.proposals.append(s)

        self.dbsession.save(s)
        self.dbsession.flush()

        vid = v.id
        stid = st.id
        sid = s.id

        self.dbsession.clear()

        print vid, stid, sid

        v = self.dbsession.get(model.Person, vid)
        st = self.dbsession.get(model.ProposalType, stid)
        s = self.dbsession.get(model.Proposal, sid)
        
        self.assertEqual(1, len(v.proposals))
        self.assertEqual(s.title, v.proposals[0].title)
        # check references
        self.assertEqual(v, v.proposals[0].people[0])
        self.assertEqual(v.handle, v.proposals[0].people[0].handle)
        self.assertEqual(st.name, v.proposals[0].type.name)

        # check the proposal relations
        self.assertEqual(st.name, s.type.name)
        self.assertEqual(v.handle, s.people[0].handle)

        print s.type
        print s.people[0]

        self.dbsession.delete(s)
        self.dbsession.delete(st)
        self.dbsession.delete(v)
        self.dbsession.flush()
        
        v = self.dbsession.get(model.Person, vid)
        self.failUnlessEqual(None, v)
        s = self.dbsession.get(model.Proposal, sid)
        self.failUnlessEqual(None, s)
        st = self.dbsession.get(model.ProposalType, stid)
        self.failUnlessEqual(None, st)
        
        self.check_empty_session()


    def test_double_person_proposal_mapping(self):
        r1 = model.Person(email_address='testguy@example.org',
                    password='p')
        r2 = model.Person(email_address='testgirl@example.com',
                    password='q')
        st = model.ProposalType('Presentation')

        self.dbsession.save(r1)
        self.dbsession.save(r2)
        self.dbsession.save(st)
        
        self.dbsession.flush()
        
        s1 = model.Proposal(title='one',
                        abstract='bar',
                        type=st)
        self.dbsession.save(s1)

        r1.proposals.append(s1)
        self.dbsession.flush()

        self.failUnless(s1 in r1.proposals)

        s2 = model.Proposal(title='two',
                        abstract='some abstract',
                        type=st)

        self.dbsession.save(s2)
        r2.proposals.append(s2)
        self.dbsession.flush()

        self.failUnless(s2 in r2.proposals)

        print "r1", r1, r1.proposals

        print "r2", r2, r2.proposals

        # assert positives
        self.failUnless(s1 in r1.proposals)
        self.failUnless(s2 in r2.proposals)

        # now make sure the converse is true
        self.failIf(s1 in r2.proposals, "invalid proposal in r2.submissions: %r" % s1)
        self.failIf(s2 in r1.proposals, "invalid proposal in r1.submissions: %r" % s2)

        # clean up
        self.dbsession.delete(s2)
        self.dbsession.delete(s1)
        self.dbsession.delete(r2)
        self.dbsession.delete(r1)
        self.dbsession.delete(st)
        self.dbsession.flush()

        # check
        self.domain = model.proposal.Proposal
        self.check_empty_session()

    def test_multiple_persons_per_proposal(self):
        p1 = model.Person(email_address='one@example.org',
                    password='foo')
        st = model.ProposalType('Presentation')
        self.dbsession.save(p1)
        self.dbsession.save(st)

        s = model.Proposal(title='a sub')
        p1.proposals.append(s)
        self.dbsession.save(s)
        self.dbsession.flush()

        p2 = model.Person(email_address='two@example.org',
                    password='bar')
        s.people.append(p2)
        self.dbsession.save(p2)
        self.dbsession.flush()

        p3 = model.Person(email_address='three@example.org',
                    password='quux')
        self.dbsession.save(p3)
        self.dbsession.flush()


        self.failUnless(s in p1.proposals)
        self.failUnless(s in p2.proposals)

        self.failUnless(p1 in s.people)
        self.failUnless(p2 in s.people)

        print "p3 subs:", p3.proposals
        print "s.people:", s.people
        self.failIf(s in p3.proposals)
        self.failIf(p3 in s.people)

        # clean up
        self.dbsession.delete(s)
        self.dbsession.delete(p1)
        self.dbsession.delete(p2)
        self.dbsession.delete(st)

        self.dbsession.flush()
        
        # check
        self.domain = model.proposal.Proposal
        self.check_empty_session()

    def test_proposal_with_attachment(self):
        p = model.Proposal(title='prop 1')
        self.dbsession.save(p)

        a = model.Attachment(filename='a',
                       content_type='text/plain',
                       creation_timestamp=datetime.datetime.now(),
                       content="foobar")
        self.dbsession.save(a)

        p.attachments.append(a)
        self.dbsession.flush()

        pid = p.id
        aid = a.id

        self.dbsession.clear()

        p = self.dbsession.get(model.Proposal, pid)
        a = self.dbsession.get(model.Attachment, aid)
        self.assertEqual(p.attachments[0], a)

        self.dbsession.delete(a)
        self.dbsession.delete(p)
        self.dbsession.flush()

        #self.assertEmptyModel(Attachment)
        #self.assertEmptyModel(Proposal)


    def test_reviewed_proposal(self):
        p1 = model.Person(email_address='one@example.org',
                    password='foo')
        st = model.ProposalType('Presentation')
        self.dbsession.save(p1)
        self.dbsession.save(st)

        s = model.Proposal(title='a sub')
        p1.proposals.append(s)
        self.dbsession.save(s)

        p2 = model.Person(email_address='reviewer@example.org',
                    password='bar')
        self.dbsession.save(p2)

        stream = model.Stream(name="pants")

        r = model.Review(reviewer=p2, stream=stream, comment="Buuzah")
        s.reviews.append(r)
        self.dbsession.save(r)
        

        self.dbsession.flush()

        self.failUnless(s in p1.proposals)
        self.failUnless(s not in p2.proposals)

        self.failUnless(p1 in s.people)
        self.failUnless(p2 not in s.people)

        self.failUnless(r in s.reviews)

        # clean up
        self.dbsession.delete(s)
        self.dbsession.delete(p1)
        self.dbsession.delete(p2)
        self.dbsession.delete(st)
        self.dbsession.delete(stream)

        self.dbsession.flush()
        
        # check
        self.domain = model.proposal.Proposal
        self.check_empty_session()
