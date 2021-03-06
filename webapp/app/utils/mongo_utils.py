# -*- coding: utf-8 -*-
class MongoUtils(object):

    mongo = None

    def __init__(self):
        pass

    def init(self, mongo):
        self.mongo = mongo

    def get_absences(self, year=None):

        docs = self.mongo.db.absence.aggregate([
            {
                "$group":{
                    "_id":{
                        "firstName": "$firstName",
                        "lastName": "$lastName"
                    },
                    "count":{
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "count": -1
                }   
            },
            {
                "$project":{
                    "_id": 0,
                    "firstName": "$_id.firstName",
                    "lastName": "$_id.lastName",
                    "count": "$count"
                }   
            }
        ])

        return docs['result']


    def get_parliament_members(self, party_type=None):

        match = {'$match': {}}

        if party_type != None:
            if party_type == 'faction':
                party_type = 'Фракция'
            
            elif party_type == 'deputies':
                party_type = 'депутатская группа'

            match = {
                '$match':{
                    'group.type': party_type
                } 
            }


        sort = {
            "$sort": {
                "absences.count": -1,
                "lastName": 1,
                "firstName": 1,
            }   
        }

        docs = self.mongo.db.deputies.aggregate([
            match,
            sort
        ])

        return docs['result']
