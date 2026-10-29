from django.db import models
'''
Name : Tim Nguyen
Email : tim7@bu.edu
Description : Loading Voter data model
'''

# Create your models here.
class Voter(models.Model):
    '''
    Stores all of our voter datta about when they have voted and info
    '''
    
    voterid = models.TextField()
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.IntegerField()
    dob = models.DateField()
    registeration = models.DateField()
    party = models.CharField()
    precinct = models.CharField()
    
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    
    voter_score = models.IntegerField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
def load_data():
    filename = "/Users/Tim/Downloads/newton_voters.csv"
    with open(filename) as f:
        headers = f.readline()
        
        for line in f:
            fields = line.strip().split(',')
            if fields[8] == "1900-01-00":
                print(line)
                continue
            else:
                try: 
                    voter =  Voter(
                        voterid = fields[0],
                        last_name = fields[1],
                        first_name = fields[2],
                        street_number = fields[3],
                        street_name = fields[4],
                        apartment_number = fields[5],
                        zip_code = fields[6],
                        dob = fields[7],
                        registeration = fields[8],
                        party = fields[9].strip(),
                        precinct = fields[10],
                        
                        v20state = fields[11] == 'TRUE',
                        v21town = fields[12] == 'TRUE',
                        v21primary = fields[13] == 'TRUE',
                        v22general = fields[14] == 'TRUE',
                        v23town = fields[15] == 'TRUE',
                        
                        voter_score = fields[16],
                    )
                    voter.save()
                except:
                    print("error")
                    print(line)
