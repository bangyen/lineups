from src import lang
import unittest
import re

class TestLanguageFunctions(unittest.TestCase):
    def test_match(self):
        def conv(s):
            l = list(s)
            return lang.match(l)

        self.assertEqual(conv('()'  ), 2)
        self.assertEqual(conv('(())'), 4)
        self.assertEqual(conv('())' ), 2)
        self.assertEqual(conv('(('  ), 3)
        self.assertEqual(conv(''    ), 1)
        self.assertEqual(conv('('   ), 2)

    def test_split(self):
        def check(s):
            return spl('foo', s)

        inp = 'foo bar'
        out = ('foo', 'bar')
        spl = lang.split

        self.assertEqual(check('foo'), ('foo', None))
        self.assertEqual(check(inp),         out)
        self.assertEqual(check('foo   bar'), out)
        self.assertEqual(check('  foo bar'), out)
        self.assertEqual(spl('^foo', inp),   out)

        self.assertIsNone(check('foobar'     ))
        self.assertIsNone(check('bar baz'    ))
        self.assertIsNone(check('baz foo'    ))
        self.assertIsNone(check('bar foo baz'))

    def test_convert(self):
        conv = lang.conv
        innr = {'foo': 'baz'}
        outr = {'bar': innr}

        toks = ['or', 'key', '=~', 'foo']
        func = [conv(t) for t in toks]

        for k in range(len(toks)):
            with self.subTest(i=toks[k]):
                self.assertTrue(callable(func[k]))

        self.assertTrue(conv('True'))
        self.assertTrue(func[0](True, False))

        self.assertEqual(conv('""'),   '')
        self.assertEqual(conv('100'), 100)
        self.assertEqual(func[1]({},   'bar'), 'bar')
        self.assertEqual(func[3](outr, 'bar'), 'baz')

        self.assertTrue(
            isinstance(
                func[2]('bar', 'b'),
                re.Match
        ))


if __name__ == '__main__':
    unittest.main()
