import sys

class BrainFuck():
    def __init__( self, bf_filename ):
        self.bfstringlist = self.runLengthEncode( open( sys.argv[1], 'r' ).read() )
        self.Clang = ""

    def toc( self, output_filename ):
        self.Clang  = ""
        self.Clang += "#include<stdio.h>\n\n"
        self.Clang += "int main() {\n"
        self.Clang += "    static char tape[10000];\n"
        self.Clang += "    int index = 0;\n\n"

        index, indent = 0, 1
        for symboltoken in self.bfstringlist:
            symbol, repeat = symboltoken[0], int(symboltoken[1:])
            if symbol == '>':
                index += repeat
            if symbol == '<':
                index -= repeat
            if symbol == '[':
                for _ in range(repeat):
                    self.Clang += '\t' * indent
                    self.Clang += "while ( tape[{0}] ) {1}\n".format( str(index), '{' )
                    indent += 1
            if symbol == ']':
                for _ in range(repeat):
                    indent -= 1
                    self.Clang += '\t' * indent
                    self.Clang += "}\n"
            if symbol == '+':
                self.Clang += '\t' * indent
                self.Clang += "tape["+ str(index) +"]"
                self.Clang += "+="+ str(repeat) +";\n" if repeat > 1 else "++;\n"
            if symbol == '-':
                self.Clang += '\t' * indent
                self.Clang += "tape["+ str(index) +"]"
                self.Clang += "-="+ str(repeat) +";\n" if repeat > 1 else "--;\n"
            if symbol == '.':
                self.Clang += '\t' * indent
                self.Clang += "printf( \"%c\",(tape["+ str(index) +"]) );\n"
            if symbol == ',':
                self.Clang += '\t' * indent
                self.Clang += "scanf( \"%c\", &tape["+ str(index) +"] );\n"

        self.Clang += "    return 0;\n}"

        output_file = open( output_filename,'w+' )
        output_file.write( self.Clang  )
        output_file.close()

    def runLengthEncode ( self, plainText ):
        count, res = '', ''
        for i in plainText:
            if i in count:
                count += i
            else:
                if len(count) > 0:
                    res += "/" + count[0] + str(len(count))
                count = i
        return res.split('/')[1:]

#main program
if __name__=="__main__":
    bf = BrainFuck( sys.argv[1] )
    bf.toc( sys.argv[2] )
