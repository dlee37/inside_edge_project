"""Main script for generating output.csv."""

import pandas as pd

def main():
    # add basic program logic here
    #path = '/home/lee/Desktop/python_hiring_test/data/raw/'

    #open dataset
    data = pd.read_csv('data/raw/pitchdata.csv')

    #get all of the subset datasets, and rename the columns to conveniently
    #join later
    hitterId = data.groupby(['HitterId','PitcherSide',],as_index=False).sum()
    hitterTeamId = data.groupby(['HitterTeamId','PitcherSide'],as_index=False).sum()
    pitcherId = data.groupby(['PitcherId','HitterSide'],as_index=False).sum()
    pitcherTeamId = data.groupby(['PitcherTeamId','HitterSide'],as_index=False).sum()
    hitterId = hitterId.loc[hitterId.PA >= 25,:]
    hitterTeamId = hitterTeamId.loc[hitterTeamId.PA >= 25,:]
    pitcherId = pitcherId.loc[pitcherId.PA >= 25,:]
    pitcherTeamId = pitcherTeamId.loc[pitcherTeamId.PA >= 25,:]
    hitterTeamId.rename(index=str,columns={'HitterTeamId':'SubjectId'},inplace=True)
    pitcherId.rename(index=str,columns={'PitcherId':'SubjectId'},inplace=True)
    pitcherTeamId.rename(index=str,columns={'PitcherTeamId':'SubjectId'},inplace=True)
    hitterId.rename(index=str,columns={'HitterId':'SubjectId'},inplace=True)
    #print(hitterId)

    #this is the final output
    output = pd.DataFrame(columns=['SubjectId','Stat','Split','Subject','Value'])

    #go through the htter lists and do calculations
    hitterList = [hitterId,hitterTeamId]
    hitterSubject = ['HitterId','HitterTeamId']
    hitterSplit = ['vs LHP','vs RHP']
    stats = ['AVG','OPB','SLG','OPS']
    for i in range(len(hitterList)):
        data = hitterList[i]
        d = 0
        for j in range(len(hitterSplit)):
            if (j == 0):
                d = data.loc[data.PitcherSide == 'L',:]
            else:
                d = data.loc[data.PitcherSide == 'R',:]
            avg = round(d.H/d.AB,3)
            opb = round((d.H + d.BB+ d.HBP)/(d.AB + d.BB + d.HBP + d.SF),3)
            slg = round((d.TB/d.AB),3)
            ops = round(slg+opb,3)
            for stat in stats:
                temp = pd.DataFrame(columns=['SubjectId','Stat','Split','Subject','Value'])
                temp.SubjectId = d.SubjectId
                temp.Stat = stat
                temp.Split = hitterSplit[j]
                temp.Subject = hitterSubject[i]
                val = 0
                if (stat == 'AVG'):
                    val = avg
                elif (stat == 'OPB'):
                    val = opb
                elif (stat == 'SLG'):
                    val = slg
                else:
                    val = ops
                temp.Value = val
                #print(temp)
                output = pd.concat([output,temp])

    #now go through the pitchers, same calulations
    pitcherList = [pitcherId,pitcherTeamId]
    pitcherSubject = ['PitcherId','PitcherTeamId']
    pitcherSplit = ['vs LHH','vs RHH']
    for i in range(len(pitcherList)):
        data = pitcherList[i]
        d = 0
        for j in range(len(hitterSplit)):
            if (j == 0):
                d = data.loc[data.HitterSide == 'L',:]
            else:
                d = data.loc[data.HitterSide == 'R',:]
            avg = round(d.H/d.AB,3)
            opb = round((d.H + d.BB+ d.HBP)/(d.AB + d.BB + d.HBP + d.SF),3)
            slg = round((d.TB/d.AB),3)
            ops = round(slg+opb,3)
            for stat in stats:
                temp = pd.DataFrame(columns=['SubjectId','Stat','Split','Subject','Value'])
                temp.SubjectId = d.SubjectId
                temp.Stat = stat
                temp.Split = pitcherSplit[j]
                temp.Subject = pitcherSubject[i]
                val = 0
                if (stat == 'AVG'):
                    val = avg
                elif (stat == 'OPB'):
                    val = opb
                elif (stat == 'SLG'):
                    val = slg
                else:
                    val = ops
                temp.Value = val
                output = pd.concat([output,temp],ignore_index=True)

    #sort and clean the dataset
    output.sort_values(by=['SubjectId','Stat','Split','Subject'],inplace=True)
    output.to_csv('data/processed/output.csv',index=False)
    orig = pd.read_csv('data/reference/output.csv')
    #print((orig.Value-output.Value)**2)

if __name__ == '__main__':
    main()
