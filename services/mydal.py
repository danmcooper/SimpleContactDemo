import redis
import sys

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def getcontacts():
    """Get a dictionary of all contacts"""
    contacts = {}

    try:
        #get list of contact ids
        contactids = r.smembers("contacts")

        #for each contact id get data
        for contactid in contactids:
            contacts.update(_getcontact(str(contactid)))
        return contacts
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

def addcontact(name, address=None, phone=None, email=None):
    """Add a contact - name is mandatory, return dictionary of new contact"""
    try:
        newid = str(r.incr("global:nextUserId"))
        _setcontact(newid, name, address, phone, email)
        r.sadd("contacts", newid)

        return _getcontact(newid)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise       

def changecontact(id, name=None, address=None, phone=None, email=None):
    """Change contact info - all fields are optional"""
    try:
        currentid = str(id)
        _setcontact(currentid, name, address, phone, email)

        return _getcontact(currentid)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

def delcontact(id):
    """Delete a contact by id"""
    delid = str(id)

    try:
        r.srem("contacts", delid, 1)

        r.delete("uid:" + delid + ":name")
        r.delete("uid:" + delid + ":address")
        r.delete("uid:" + delid + ":phone")
        r.delete("uid:" + delid + ":email")

        return {}
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise   

def _getcontact(id):
    """Helper to get a contact dictionary"""
    contact = {}
    idwrapper = {}
    
    try:
        contact["name"] = r.get("uid:" + id + ":name")
        contact["address"] = r.get("uid:" + id + ":address")
        contact["phone"] = r.get("uid:" + id + ":phone")
        contact["email"] = r.get("uid:" + id + ":email")
        idwrapper[id] = contact

        return idwrapper
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

def _setcontact(id, name=None, address=None, phone=None, email=None):
    """Helper to set a contact dictionary"""
    try:
        if name is not None:
            r.set("uid:" + id + ":name", name)
        if address is not None:         
            r.set("uid:" + id + ":address", address)
        if phone is not None:       
            r.set("uid:" + id + ":phone", phone)
        if email is not None:       
            r.set("uid:" + id + ":email", email)

        return True
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise       