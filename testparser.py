from lslopt.lslparse import parser,EParseSyntax,EParseUEOF,EParseAlreadyDefined,\
    EParseUndefined,EParseTypeMismatch,EParseReturnShouldBeEmpty,EParseReturnIsEmpty,\
    EParseInvalidField,EParseFunctionMismatch,EParseDeclarationScope,\
    fieldpos
from lslopt.lsloutput import outscript
from lslopt.lsloptimizer import optimizer
from lslopt import lslfuncs
import unittest
import os

class UnitTestCase(unittest.TestCase):
    pass

class Test01_LibraryLoader(UnitTestCase):
    def test_coverage(self):
        os.remove('builtins.txt')
        f = open('builtins.txt', 'wb')
        f.write(r'''const key a="\t"
event ev(integer i)
event ev(integer i)
quaternion x(integer i)
void x(integer i)
blah
const vector a = <4,5,3,2>
const vector a = <4,5,3,2
const vector a = <x,4,3>
const vector a = <4,x,3>
const vector a = <3,4,x>
const rotation a = <3,4,4,x>
const list l = []
const quaternion q=<1,2,3,4>
const string v="
const string q="\t"
''')
        f.close()
        parser()
        f = open('builtins.txt.dat', 'rb')
        b = f.read()
        f.close()
        os.remove('builtins.txt')
        f = open('builtins.txt', 'wb')
        f.write(b)
        f.close()
        parser()


class Test02_Compiler(UnitTestCase):
    def setUp(self):
        self.parser = parser()
        self.outscript = outscript()

    def test_coverage(self):
        try:
            os.remove('overwritten.lsl')
        except OSError:
            pass
        f = open('overwritten.lsl', 'wb')
        f.write('/*Autogenerated*/default{timer(){}}')
        f.close()
        del f
        self.parser.parsefile('overwritten.lsl')
        self.outscript.output(self.parser.parse("""default{touch(integer n){jump n;@n;}}"""))
        self.assertRaises(EParseUndefined, self.parser.parse, """default{touch(integer n){jump k;n;}}""")
        self.outscript.output(self.parser.parse("""default{touch(integer n){n;}}"""))
        print self.outscript.output(self.parser.parse(r"""string x="";
            vector V=ZERO_VECTOR;
            vector W = <1,2,3>;
            quaternion Q = <1,2,3,4>;
            float f;
            float ff = f;
            list L = [];
            list L2 = [2,3,4,5,-6];
            list L3 = [2,3,f,5,-6.0];
            rotation QQ = <f,f,f,f>;
            integer fn(integer x){
                if (1) for (f=3,f=4,f=5;3;f++,f++) do while(0); while(0); else if (2) return 2; else;
                fn(3);
                integer j = 3||4&&5|6^7&8.==9!=10.e+01f<11<=12>13.>=14<<15>>16== ++f+-f++;
                j *= 3.0; // LSL allows this
                1+((float)2+(integer)(1+1));
                12345678901;0x000000012345678901;0x000;
                2*(V*V/4)*V*--V.x*V.x++;
                L+L2;L+1;1+L;
                <0,0,0.>0>0>*<0,0,0==0>2,3>>3>3.>%<3,4,5>;
                f -= TRUE-(integer)-1;
                f *= !FALSE;
                V %= (ZERO_VECTOR+-ZERO_VECTOR)*(ZERO_ROTATION+-ZERO_ROTATION);
                1e37;1.1e22;1.;
                print(V *= 3);
                fwd("","","");
                L"\n\t\rxxxx";@lbl;jump lbl;
                {f;}
                [1,2,3];
            }
            fwd(string a,string b,string c){}
            default{touch(integer n){n;state default;state another;return;}timer(){}}
            state another{timer(){}}//"""))
        self.assertRaises(EParseUEOF, self.parser.parse, '')
        self.assertRaises(EParseUEOF, self.parser.parse, 'default')
        self.assertRaises(EParseSyntax, self.parser.parse, 'x')
        self.outscript.output(self.parser.parse('integer x=TRUE;integer y=x;integer j=FALSE;default{timer(){}}'))
        self.assertRaises(EParseSyntax, self.parser.parse, ';')
        self.assertRaises(EParseSyntax, self.parser.parse, 'f(){}g(integer x,key y){{}}h(;){}')
        self.assertRaises(EParseSyntax, self.parser.parse, 'f(){}g(integer x,key y){}h()}')
        self.assertRaises(EParseUEOF, self.parser.parse, 'integer "')
        self.assertRaises(EParseSyntax, self.parser.parse, 'default{timer(){}}state blah{timer(){}}state ;')
        self.assertRaises(EParseSyntax, self.parser.parse, 'default{timer(integer x){}}')
        self.assertRaises(EParseSyntax, self.parser.parse, 'default{timer(integer x){(integer)x=0}}')
        self.assertRaises(EParseSyntax, self.parser.parse, 'default{timer(){state;}}')
        self.assertRaises(EParseAlreadyDefined, self.parser.parse, 'default{timer(integer x,integer x){}}')
        self.assertRaises(EParseSyntax, self.parser.parse, 'x;')
        self.assertRaises(EParseSyntax, self.parser.parse, '1e;')
        self.assertRaises(EParseSyntax, self.parser.parse, 'integer x=-TRUE;')
        self.assertRaises(EParseSyntax, self.parser.parse, 'integer x=-3;integer y=-x;')
        self.assertRaises(EParseAlreadyDefined, self.parser.parse, '''float x=3;float x;''')
        self.assertRaises(EParseAlreadyDefined, self.parser.parse, '''default{timer(){}}
            state blah{timer(){}}
            state blah{}''')
        self.assertRaises(EParseAlreadyDefined, self.parser.parse, '''default{timer(){@x;@x;}}''')
        self.assertRaises(EParseAlreadyDefined, self.parser.parse, '''default{timer(){integer x;@x;}}''')
        self.assertRaises(EParseAlreadyDefined, self.parser.parse, '''default{timer(){@x;integer x;}}''')
        self.assertRaises(EParseUEOF, self.parser.parse, 'float x=3+3;', set(('extendedglobalexpr',)))
        self.assertRaises(EParseUndefined, self.parser.parse, '''float x=-2147483648;float y=z;''')
        self.assertRaises(EParseUndefined, self.parser.parse, '''float z(){;}float y=z;''')
        self.assertRaises(EParseUndefined, self.parser.parse, '''float y=z;float z;''')
        self.assertRaises(EParseUndefined, self.parser.parse, '''default{timer(){state blah;}}''')
        self.assertRaises(EParseUndefined, self.parser.parse, '''f(){k;}''')
        self.assertRaises(EParseReturnShouldBeEmpty, self.parser.parse, '''default{timer(){return 1;}}''')
        self.assertRaises(EParseReturnIsEmpty, self.parser.parse, '''integer f(){return;}''')
        self.assertRaises(EParseFunctionMismatch, self.parser.parse, '''f(integer i){f("");}''')
        self.assertRaises(EParseFunctionMismatch, self.parser.parse, '''f(integer i){f(1,2);}''')
        self.assertRaises(EParseFunctionMismatch, self.parser.parse, '''f(integer i){f(f(1));}''')
        self.assertRaises(EParseFunctionMismatch, self.parser.parse, '''f(integer i){f();}''')
        self.assertRaises(EParseDeclarationScope, self.parser.parse, '''f(){if (1) integer i;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){[f()];}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){3.||2;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){3||2.;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){3.|2;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){3|2.;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){3.&2;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){3&2.;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){3.^2;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){3^2.;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){f()!=2;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){2!=f();}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){3.<"";}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){""<"".;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){3.<<2;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){3>>2.;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){""-(key)"";}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){""+f();}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){""+(key)"";}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){(key)""+"";}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){(key)""+(key)"";}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){key k;k+k;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){3/<1,2,3>;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){3/<1,2,3,4>;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){""*3;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){""%4;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){3%<2,3,4>;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){""%4;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){float i;i%=2;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){float i;i&=2;}''', ['extendedassignment'])
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){(vector)4;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){key k;k+=k;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){string i;i++;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){string i;(i-=i);}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){string i;(i*=i);}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){string i;-i;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){string i;~i;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){string i;!i;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){string i;++i;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''g(){integer k;k=g();}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''g(){@x;x;}state x{}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''g(){print(g());}state x{}''')
        self.assertRaises(EParseUndefined, self.parser.parse, '''g(){integer k;k();}''')
        self.assertRaises(EParseUndefined, self.parser.parse, '''g(){++x;}state x{}''')
        self.assertRaises(EParseUndefined, self.parser.parse, '''g(){print(x);}state x{}''')
        self.assertRaises(EParseUEOF, self.parser.parse, '''f(){(integer)''')
        self.assertRaises(EParseInvalidField, self.parser.parse, '''f(){vector v;v.s;}''')
        self.assertRaises(EParseSyntax, self.parser.parse, '''f(){<1,2,3,4==5>;}''')
        self.assertRaises(EParseSyntax, self.parser.parse, '''#blah;\ndefault{timer(){}}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){<1,2,3,4>"">;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){<1,2,3,"">"">;}''')
        self.assertRaises(EParseTypeMismatch, self.parser.parse, '''f(){string i;(i&=i);}''',
            set(('extendedassignment')))

        self.assertRaises(EParseUndefined, self.parser.parse, '''key a=b;key b;default{timer(){}}''',
            ['extendedglobalexpr'])
        # Force a list constant down its throat, to test coverage of LIST_VALUE
        self.parser.constants['LISTCONST']=[1,2,3]
        print self.outscript.output(self.parser.parse('default{timer(){LISTCONST;}}'))

        print self.outscript.output(self.parser.parse('''string s="1" "2";default{timer(){}}''',
            ['allowmultistrings'])) # the one below doesn't work because it uses extended global expr.
        print self.outscript.output(self.parser.parse('''
            float f=2+2;
            #blah;
            string s = "1" "2";
            list L = [(key)""];
            default{timer(){
            1+([]+(integer)~1);
            list a;
            float f;
            a = 3; a += 3;
            f += 4; f += -4.3;
            integer i;
            i |= i;
            "a" "b" "c";
            "a"+(key)"b"; (key)"a" + "b";
            i>>=i;
            }}''',
            ['explicitcast','extendedtypecast','extendedassignment',
                'extendedglobalexpr', 'allowmultistrings', 'allowkeyconcat',
                'skippreproc']
            ))
        print self.parser.scopeindex
        #self.assertRaises(EParseUnexpected, self.parser.PopScope)

        self.assertEqual(fieldpos("a,b",",",3),-1)
        self.assertEqual(self.outscript.Value2LSL(lslfuncs.Key(u'')), '((key)"")')
        self.assertRaises(AssertionError, self.outscript.Value2LSL, '')

    def tearDown(self):
        del self.parser
        del self.outscript

class Test03_Optimizer(UnitTestCase):
    def setUp(self):
        self.parser = parser()
        self.opt = optimizer()
        self.outscript = outscript()

    def test_coverage(self):
        p = self.parser.parse('''
            float f=2+llAbs(-2);
            float g = f;
            string s = "1" "2";
            list L = [(key)""];
            list L1 = L;
            list L2 = [1,2,3,4,5,6.0];
            list L3 = [];
            vector v=<1,2,f>;
            float ffff2 = v.x;
            vector vvvv = <1,2,llGetNumberOfSides()>;
            float ffff=vvvv.x;
            vector vvvv2=vvvv;
            float ffff3 = v.z;
            integer fn(){return fn();}

            default{touch(integer n){
                1+([]+(integer)~1);
                list a;
                float f;
                vector v=<1,2,f>;<1,2,3>;<1,2,3,4>;v.x;
                v-<0,0,0>;<0,0,0>-v;v+<0,0,0>;<0,0,0>+v;
                []+f;
                integer j = 3||4&&5|6^7&8.==9!=10.e+01f<11<=12>13.>=14<<15>>16==0&&3==
                    ++f-f++-(3 + llFloor(f)<<3 << 32) - 2 - 0;
                integer k = 2 + (3 * 25 - 4)/2 % 9;
                a = 3; a += !3;
                f += 4; f += -4.3;
                integer i;
                i = llGetListLength(L);
                print(3+2);
                for(i=3,i;1;){}
                i |= !i;
                "a" "b" "c";
                "a"+(key)"b"; (key)"a" + "b";
                llUnescapeURL("%09");
                i>>=i;
                if (1) do while (0); while (0); if (0); if (0);else; for(;0;);
                if (i) if (i); else ; while (i) ; do ; while (i); for(;i;);
                do while (1); while(1); for(;1;);
                for (i=0,i;0;);for(i=0,i=0;0;);return;
                (i-i)+(i-3)+(-i+i)+(-i-i)+(i+1)+(-i+1)+(i-1)+(-i-1)+(0.0+i);
                ((-i)+j);((-i)+i);i-2;-i-2;2-i;
            }}''',
            ['explicitcast','extendedtypecast','extendedassignment',
                'extendedglobalexpr', 'allowmultistrings', 'allowkeyconcat']
            )
        self.opt.optimize(p)
        self.opt.optimize(p, ())
        print self.outscript.output(p)
        p = self.parser.parse('''string s = llUnescapeURL("%09");default{timer(){float f=llSqrt(-1);
            integer i;-(-(0.0+i));!!(!~~(!(i)));[]+i;}}''',
            ['extendedtypecast','extendedassignment',
                'extendedglobalexpr', 'allowmultistrings', 'allowkeyconcat']
            )
        self.opt.optimize(p, ['optimize','foldtabs'])
        print self.outscript.output(p)
    def test_regression(self):


        p = self.parser.parse('''
            integer a;
            x() { if (1) { string s = "x"; s = s + (string)a; } }
            default { timer() { } }
            ''', ['extendedassignment'])
        self.opt.optimize(p)
        out = self.outscript.output(p)
        self.assertEqual(out, 'integer a;\nx()\n{\n    {\n        '
            'string s = "x";\n        s = s + (string)a;\n    }\n}\n'
            'default\n{\n    timer()\n    {\n    }\n}\n'
            )

        p = self.parser.parse(
            '''key k = "blah";
            list L = [k, "xxxx", 1.0];
            float f;
            vector v = <f, 3, 4>;

            default{timer(){}}
            ''', ['extendedassignment'])
        self.opt.optimize(p)
        out = self.outscript.output(p)
        self.assertEqual(out, 'key k = "blah";\nlist L = [k, "xxxx", 1.];\n'
            'float f;\nvector v = <0, 3, 4>;\n'
            'default\n{\n    timer()\n    {\n    }\n}\n'
            )


        p = self.parser.parse('list L;float f=llList2Float(L, 0);default{timer(){}}',
            ['extendedglobalexpr'])
        self.opt.optimize(p)
        out = self.outscript.output(p)
        print out
        self.assertEqual(out, 'list L;\nfloat f = 0;\n'
            'default\n{\n    timer()\n    {\n    }\n}\n')


    def tearDown(self):
        del self.parser
        del self.opt
        del self.outscript


if __name__ == '__main__':
    unittest.main()
