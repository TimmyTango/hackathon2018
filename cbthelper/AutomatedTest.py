from . import globals as G
from .Snapshot import Snapshot
import requests, os

class AutomatedTest:
    def __init__(self, testId):
        self.testId = testId
    def setScore(self, score):
        options = {
            'action': 'set_score',
            'score': score
        }
        requests.put(G.api + self.testId, auth=(G.username, G.authkey), data=options)
    def setDescription(self, description):
        options = {
            'action': 'set_description',
            'description': description
        }
        requests.put(G.api + self.testId, auth=(G.username, G.authkey), data=options)
    def stop(self, score=''):
        # score is optional, will combine setScore and stopTest
        if score != '':
            self.setScore(score)
        requests.delete(G.api + self.testId, auth=(G.username, G.authkey))
    def takeSnapshot(self, description=''):
        hash = requests.post(G.api + self.testId + '/snapshots', auth=(G.username, G.authkey)).json()['hash']
        snap = Snapshot(hash, self)
        if description != '':
            snap.setDescription(description)
        return snap
    def getSnapshots(self):
        snaps = requests.get(G.api+ self.testId + '/snapshots', auth=(G.username, G.authkey)).json()
        ret = []
        for snap in snaps:
            ret.append(Snapshot(snap['hash'], self))
        return ret
    def saveAllSnapshots(self, directory, prefix='image', useDescription=False):
        snaps = self.getSnapshots()
        self.__makeDirectory(directory)
        for i in range(len(snaps)):
            if useDescription and snaps[i].info['description'] != '':
                img = snaps[i].info['description'] + '.png'
            else:
                img = prefix + str(i) + '.png'
            snaps[i].saveSnapshot(os.path.join(directory, img))
    def __makeDirectory(self, dir):
        if not os.path.exists(dir):
            os.mkdir(dir)