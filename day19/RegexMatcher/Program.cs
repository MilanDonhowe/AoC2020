using System;
using System.Text.RegularExpressions;

namespace RegexMatcher
{
    class Program
    {
        static int Main(string[] args)
        {
            if (args.Length != 2){
                Console.WriteLine("Invalid Number of arguments, proper usage: <pattern> <text>");
                return 0;
            }
            if (Regex.IsMatch(args[1], args[0])){
              return 1;
            }
            return 0;
        }
    }
}
