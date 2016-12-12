# -*- coding: utf-8 -*-
import PyV8, codecs
uin = '634569405'
ptwebqq = '8ee973c75502a44b9834557d4fbb408d363a02c5adafc6f6f6fb3e0dd14f937a'
def gethash(selfuin, ptwebqq):
    selfuin += ""
    N=[0,0,0,0]
    for T in range(len(ptwebqq)):
        N[T%4]=N[T%4]^ord(ptwebqq[T])
    U=["EC","OK"]
    V=[0, 0, 0, 0]
    V[0]=int(selfuin) >> 24 & 255 ^ ord(U[0][0])
    V[1]=int(selfuin) >> 16 & 255 ^ ord(U[0][1])
    V[2]=int(selfuin) >>  8 & 255 ^ ord(U[1][0])
    V[3]=int(selfuin)       & 255 ^ ord(U[1][1])
    U=[0,0,0,0,0,0,0,0]
    U[0]=N[0]
    U[1]=V[0]
    U[2]=N[1]
    U[3]=V[1]
    U[4]=N[2]
    U[5]=V[2]
    U[6]=N[3]
    U[7]=V[3]
    N=["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    V=""
    for T in range(len(U)):
        V+= N[ U[T]>>4 & 15]
        V+= N[ U[T]    & 15]
    return V

print gethash(uin, ptwebqq)

extSrc = '''
function u(x, I) {
            x += "";
            for (var N = [], T = 0; T < I.length; T++)
                N[T % 4] ^= I.charCodeAt(T);
            var U = ["EC", "OK"], V = [];
            V[0] = x >> 24 & 255 ^ U[0].charCodeAt(0);
            V[1] = x >> 16 & 255 ^ U[0].charCodeAt(1);
            V[2] = x >> 8 & 255 ^ U[1].charCodeAt(0);
            V[3] = x & 255 ^ U[1].charCodeAt(1);
            U = [];
            for (T = 0; T < 8; T++)
                U[T] = T % 2 == 0 ? N[T >> 1] : V[T >> 1];
            N = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"];
            V = "";
            for (T = 0; T < U.length; T++) {
                V += N[U[T] >> 4 & 15];
                V += N[U[T] & 15]
            }
            return V
        }
'''
def testExtension():
    # extSrc = codecs.open(r'encrypt_test.js', mode='rb').read()
    # global extSrc
    # extSrc = """function hello(name) { return "hello " + name + " from javascript"; }"""
    extJs = PyV8.JSExtension("u/javascript", extSrc)
    with PyV8.JSContext(extensions=['u/javascript']) as ctxt:
        print ctxt.eval('''u("%s", "%s")'''% (uin, ptwebqq))

testExtension()

def testNullInString():
    with PyV8.JSContext() as ctxt:
        fn = ctxt.eval("(%s)" % extSrc)
        print fn(uin, ptwebqq)
testNullInString()

def testMultiDimArray(self):
    with PyV8.JSContext() as ctxt:
        ret = ctxt.eval("""
            ({
                'test': function(){
                    return  [
                        [ 1, 'abla' ],
                        [ 2, 'ajkss' ],
                    ]
                }
            })
            """).test()

        self.assertEquals([[1, 'abla'], [2, 'ajkss']], convert(ret))

def testJSFunction(self):
    with PyV8.JSContext() as ctxt:
        hello = ctxt.eval("(function (name) { return 'hello ' + name; })")

        self.assertEquals("hello flier", hello('flier'))
        self.assertEquals("hello flier", hello.invoke(['flier']))

        obj = ctxt.eval("({ 'name': 'flier', 'hello': function (name) { return 'hello ' + name + ' from ' + this.name; }})")
        hello = obj.hello
        self.assertEquals("hello flier from flier", hello('flier'))

        tester = ctxt.eval("({ 'name': 'tester' })")
        self.assertEquals("hello flier from tester", hello.invoke(tester, ['flier']))
        self.assertEquals("hello flier from json", hello.apply({ 'name': 'json' }, ['flier']))


extSrc = """function hello(name) { return "hello " + name + " from javascript"; }"""
extJs = PyV8.JSExtension("hello/javascript", extSrc)
with PyV8.JSContext(extensions=['hello/javascript']) as ctxt:
           print ctxt.eval("hello('flier')")
