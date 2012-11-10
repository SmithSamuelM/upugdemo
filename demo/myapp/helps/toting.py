""" toting.py
    Tote object class provides Json (de)serialization to an objects attributes.
    
"""
import sys
import os
import errno

if sys.version_info[1] < 7: #python 2.6 or earlier
    from  ordereddict import OrderedDict
else:
    from collections import OrderedDict

import json
import inspect

_debug = False

class Tote(object):
    """ Tote
        Provides Json (de)serialization capabilities to python objects.
        Use as base class.
        Suports json serialization/deserialization of instance
        attributes (not methods).
        
        All method names start with underscore so as not to preclude any public
            attribute names.

        (De)Serialization (source)target is json object string 

        If an attribute value is not json serializible it will skip it.

        Deserialization patches onto an existing tote only preexisting attributes.
        This prevents corruption or leakage of new attributes from stale serialized
        strings. This makes it easy to update an object definition by changing
        attributes but still load common attributes from an old serialization.

        Also the behavior for mangled attributes may be unexpected in some cases.

    """
    
    def _reloadable(self, keys=None, subkeys=None, recursively=False,
                    safely=False, privily=False, properly=False):
        """ Return OrderedDict of round trippable attributes (dumpable and reloadable via
            json (de)serialization), named in in keys list.
            The intent is to return items that could be round tripped.

            If keys is None (default None) then include all (de)serializable
               attributes otherwise only consider names in keys.
            If safely (default False) then exclude non-json (de)serializible items by
               checking if serialization would fail. This may be computationally
               expensive in some cases.
               By appriopriate use of keys one may choose to disable safely checking.
            If privily (default False)  include
                instance attributes that start with underscore.
            If properly (default False) include properties.
            
            Typically items from .__dict__ are used to determine which
            attributes are settable. If its in .__dict__ it had to have been
            set on the instance.
            This typically means that class attributes, properties and
            other descriptors will be excluded from reloadable.
            However if properly is true then properties not in .__dict__ but
            in dir() as characterized by inspect.isdatadescriptor()=True will also
            be included. It may be problematic if both privily and properly
            are True at the same time.

            Special attributes and functions are always excluded.
            
            If recursively (default False) then recursively apply _reloadable
            to any attributes that are Tote subclasses with subkeys. subkeys is
            a dict of tuples. The keys in subkeys correspond to Tote attributes
            of the tote instance. The value of each key, if any, in subkeys is a tuple, where
            the first element is a list (possibly None) and the second element is
            a subkeys dictionary for the Tote attributes of the Tote attribute named
            by the subkeys key. This allows recusive application of keys.


        """
        attrs = self.__dict__.keys()
        
        if properly:
            props = [key for key in dir(self) if hasattr(self.__class__, key) and 
                     inspect.isdatadescriptor(getattr(self.__class__, key))]
            if props:
                attrs.extend(props)
        
        if keys == None:
            keys = sorted(attrs)
        else: #filter on both keys and attrs
            keys = [key for key in keys if key in attrs]        

        reloadable = OrderedDict() #use odict so serialization is ordered

        for name in keys:  #build nested OrderedDict of serializible attributes      
            if name.startswith('__') and name.endswith('__'):
                continue #skip special attributes
            if not privily and name.startswith('_'): #skip private
                continue
            try: #skip if fails getattr which includes mangled in some cases
                attr = getattr(self, name)
            except AttributeError as ex:
                continue
            if inspect.isroutine(attr): #skip methods
                continue
            if recursively and isinstance(attr, Tote): #recusively dump tote attributes
                if subkeys:
                    attrkeys, attsubkeys = subkeys.get(name, (None, None))
                else:
                    attrkeys = attsubkeys = None
                    
                reloadable[name] = attr._reloadable(keys=attrkeys, subkeys=attsubkeys,
                                safely=safely, privily=privily, properly=properly)
                continue
            if safely:
                try: #last resort, skip attributes that are not json serializible
                    temp = json.dumps(attr)
                except TypeError as ex:
                    continue
            reloadable[name] = attr #valid attribute
        return reloadable

    def _dumpable(self, keys=None, subkeys=None, recursively=False,
                  safely=False, privily=False):
        """ Return OrderedDict of attributes dumpable but not necessarily reloadable (via
            json (de)serialization) named in in keys list.
            Uses dir() as source of dumpable attributes but excluding excluding
            special attributes and functions. This could include all getable
            properties and class attributes.
            Thus there is no expectation that these are round trippable.

            If keys is None (default None) then include all serializable
               attributes otherwise only consider names in keys.
            If safely (default False) then exclude non-json serializible items by
               checking if serialization would fail. This may be computationally
               expensive in some cases.
               By appriopriate use of keys one may choose to disable safely checking.
            If privily (default False)  include gettable
                attributes that start with underscore.
            If recursively (default False) then recursively apply _reloadable
            to any attributes that are Tote subclasses with subkeys. subkeys is
            a dict of tuples. The keys in subkeys correspond to Tote attributes
            of the tote instance. The value of each key, if any, in subkeys is a tuple, where
            the first element is a list (possibly None) and the second element is
            a subkeys dictionary for the Tote attributes of the Tote attribute named
            by the subkeys key. This allows recusive application of keys.

        """
        if keys == None:
            keys = sorted(dir(self))
        else: #filter on both keys and dir(self)
            keys = [key for key in keys if key in dir(self)]        
        dumpable = OrderedDict() #use odict so serialization is ordered
        for name in keys:  #build nested OrderedDict of serializible attributes      
            if name.startswith('__') and name.endswith('__'):
                continue #skip special attributes            
            if not privily and name.startswith('_'): #skip private
                continue
            try: #skip if fails getattr which includes mangled in some cases
                attr = getattr(self, name)
            except AttributeError as ex:
                continue
            if inspect.isroutine(attr): #skip methods
                continue
            if recursively and isinstance(attr, Tote): #recusively dump tote attributes
                if subkeys:
                    attrkeys, attsubkeys = subkeys.get(name, (None, None))
                else:
                    attrkeys = attsubkeys = None                
                dumpable[name] = attr._dumpable(keys=attrkeys, subkeys=attsubkeys,
                                                safely=safely, privily=privily) 
                continue
            if safely:
                try: #last resort, skip attributes that are not json serializible
                    temp = json.dumps(attr)
                except TypeError as ex:
                    continue
            dumpable[name] = attr #valid attribute
        return dumpable    

    def _revise(self, it, keys=None, subkeys=None, recursively=False,
                safely=False, privily=False, properly=False):
        """ Update settable serializible attributes in keys from items in it
            Returns False if failure

            If keys is None (default None) then include all serializible attributes.
            if safely (default False) then test existing attributes for serializiblilty
               before patching from it. This is slower.
            If privily (default False) then update
                instance attributes that start with underscore
            If properly (default False) include properties

            Typically items from .__dict__ are used to determine which
            attributes are settable. If its in .__dict__ it had to have been
            set on the instance.
            This typically means that properties and
            other descriptors will be excluded when patching.
            However if properly is true then properties not in .__dict__ but
            in dir() as characterized by inspect.isdatadescriptor()=True will also
            be patched. It may be problematic if both privily and properly
            are True at the same time.
            
            Special attributes and functions are always excluded.
            
            If recursively (default False) then recursively apply _reloadable
            to any attributes that are Tote subclasses with subkeys. subkeys is
            a dict of tuples. The keys in subkeys correspond to Tote attributes
            of the tote instance. The value of each key, if any, in subkeys is a tuple, where
            the first element is a list (possibly None) and the second element is
            a subkeys dictionary for the Tote attributes of the Tote attribute named
            by the subkeys key. This allows recusive application of keys.


        """
        if not hasattr(it, 'get'): #it not a dictionary
            return False
        if keys == None:
            keys = self.__dict__.keys()
        else: #filter in both keys and self.__dict__
            keys = [key for key in keys if key in self.__dict__]
        if properly:
            props = [key for key in dir(self) if hasattr(self.__class__, key) and 
                     inspect.isdatadescriptor(getattr(self.__class__, key))]
            if props:
                keys.extend(props)   
        for key, value in it.items():
            if key not in keys: 
                continue #skip if not preexisting instance attribute
            if key.startswith('__') and key.endswith('__'):
                continue #skip special attributes
            if not privily and key.startswith('_'):
                continue #skip private attribute if not privily
            try: #skip if fails getattr which includes mangled in some cases
                attr = getattr(self, key)
            except AttributeError as ex:
                continue
            if inspect.isroutine(attr): #skip methods
                continue
            if recursively and isinstance(attr, Tote): #recursively load tote attributes
                if subkeys:
                    attrkeys, attsubkeys = subkeys.get(key, (None, None))
                else:
                    attrkeys = attsubkeys = None                   
                attr._revise(value, keys=attrkeys, subkeys=attsubkeys,
                             safely=safely, privily=privily, properly=properly) 
                continue
            if safely:
                try: #last resort, skip attributes that are not json serializible
                    temp = json.dumps(attr)
                except TypeError as ex:
                    continue
            setattr(self, key, value)  #update attribute
        return True

    def _dumps(self, it):
        """ Return json serialized string version of it
            Returns None if serialization failed
        """
        try:
            return( json.dumps(it, indent=2))
        except TypeError as ex:
            return None

    def _loads(self, s):
        """ Return deserialized python object (dict) from json serialized string s
            Returns None if failure
        """
        try:
            return json.loads(s)
        except ValueError as ex:
            return None
        
    def _dump(self, it = None, filename = ""):
        """ Json serialize it and save to file filename"""
        if not it:
            raise ParameterError, "No object to Dump: %s" % str(it)
        if not filename:
            raise ParameterError, "No filename to Dump to: %s" % file
        
        with Tote._OpenOrCreateFile(filename, "w+") as f:
            json.dump(it, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        
    def _load(self, filename = ""):
        """ Loads json object from filename, returns unjsoned object"""
        if not filename:
            raise ParameterError, "Empty filename to load."
    
        with Tote._OpenOrCreateFile(filename) as f:
            try:
                it = json.load(f)
            except EOFError:
                return None
            except ValueError:
                return None
            return it

    @staticmethod
    def _OpenOrCreateFile(filename, openMode = 'r+'):
        """ Atomically create file from filename if not exists otherwise open
            IF file already exists, opens file using openMode 
            Else creates file for write update 
            Returns file object
        """
        try:
            newfd = os.open(filename, os.O_EXCL | os.O_CREAT | os.O_RDWR, 0664)
            newfile = os.fdopen(newfd,"w+")
        except OSError as ex:
            if ex.errno == errno.EEXIST:
                newfile = open(filename,openMode)
            else:
                raise 
        return newfile
    
