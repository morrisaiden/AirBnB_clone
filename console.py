#!/usr/bin/python3
"""Defines the AirBnB_clone console.

The shlex module provides a simple lexical analyzer
for splitting strings into tokens.
The split function specifically splits a string into a list of tokens
according to the syntax rules similar to those used by the Unix shell.
It's particularly useful for parsing command-line strings into individual arguments.
"""

import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    """
    Parses a string arg containing command-line arguments,
    while also handling additional syntax for tokens enclosed within curly braces {}
    or square brackets [].
    It returns a list of parsed tokens, with any enclosing braces or
    brackets included as separate tokens.
    """

    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [z.strip(",") for z in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [z.strip(",") for z in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [z.strip(",") for z in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """
    Defines the HolbertonBnB command interpreter.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        
        pass

    def default(self, arg):
        """
        Handle commands that don't match any specific methods defined within the class

        Parse a command string, extract a sub-command and its arguments, and then execute
        the corresponding method if available, or
        prints an error message if the command is not recognized.
        """

        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """
        exit cmd
        """

        return True

    def do_EOF(self, arg):
        """
        EOF signal to exit the program
        """

        print("")
        return True

    def do_create(self, arg):
        """
        This method validates the input, creates an instance of the class,
        prints its ID, and saves it into storage.
        """

        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argl[0])().id)
            storage.save()

    def do_show(self, arg):
        """
        Do_show method validates input, retrieves instances from storage,
        and prints the string representation of a specified instance if it exists
        """

        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
        """
        The do_destroy method validates input, removes the specified
        instance from storage if it exists, and saves the updated state of the storage.
        """

        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """
        The do_all method allows users to retrieve string representations of
        all instances or instances of a specific class.
        """

        argl = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """
        The do_update method has three different usages:

        update <class> <id> <attribute_name> <attribute_value>
        <class>.update(<id>, <attribute_name>, <attribute_value>)
        <class>.update(<id>, <dictionary>)

        Method allows users to update attributes of instances of a given class
        by specifying the class name, instance ID, attribute name, and attribute value,
        or by providing a dictionary of attribute names and values.
        """

        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for q, r in eval(argl[2]).items():
                if (q in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[q]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[q])
                    obj.__dict__[q] = valtype(r)
                else:
                    obj.__dict__[q] = r
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
