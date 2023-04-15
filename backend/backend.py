
from os import system
from flask import Flask, jsonify, request, json, Response
from flask_mysqldb import MySQL
from flask_cors import CORS
import MySQLdb.cursors
from json import dumps
import configparser
import os
from flask import redirect, url_for, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/media'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app=Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


config = configparser.ConfigParser()
config.read('config.ini')



app.secret_key = 'secret key'

app.config['MYSQL_HOST'] = config['mysqlDB']['host']
app.config['MYSQL_PORT'] = int(config['mysqlDB']['port'])
app.config['MYSQL_USER'] = config['mysqlDB']['user']
app.config['MYSQL_PASSWORD'] = config['mysqlDB']['pass']
app.config['MYSQL_DB'] = config['mysqlDB']['db']

mysql = MySQL(app)


@app.route("/")
def hello():
    # return "Hello Worlds!"
    return redirect("https://www.team195.com/scouting-data")

@app.route("/harish/")
def hello2():
    return "Hello Harish!!!"

#order:
#simple tables?? - 
#web app - 
#web dev - 


   
    # get event info 
@app.route("/event/", methods =['GET', 'POST'])
def get_event():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from events; ")
    data = cursor.fetchall()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response




# get scouter info
@app.route("/scouters/", methods = ['GET', 'POST']) 
def get_scouters():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select s.scouterID, s.firstName, s.lastName "
    "from scouters s; ")
    data = cursor.fetchall()
    response = app.response_class(

        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

# Get drive base types 
@app.route("/drivebasetypes/", methods =['GET', 'POST'])
def get_drivebasetypes():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT d.* "
    "FROM driveBaseTypes d; ")
    data = cursor.fetchall()
    response = app.response_class(

        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

# Get drive motor types 
@app.route("/drivemotortypes/", methods =['GET', 'POST'])
def get_drivemotortypes():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT d.* "
    "FROM driveMotorTypes d; ")
    data = cursor.fetchall()
    response = app.response_class(

        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/alliance/", methods =['GET', 'POST'])
def get_alliance():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM allianceStations; ")
    data = cursor.fetchall()
    response = app.response_class(

        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

# Get manipulator types 
@app.route("/manipulatortypes/", methods =['GET', 'POST'])
def get_manipulatortypes():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT m.* "
    "FROM manipulatorTypes m; ")
    data = cursor.fetchall()
    response = app.response_class(

        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

# Get super climb types 
@app.route("/superclimbtypes/", methods =['GET', 'POST'])
def get_superclimbtypes():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT s.* "
    "FROM superClimbTypes s; ")
    data = cursor.fetchall()
    response = app.response_class(

        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

# Get build types 
@app.route("/buildtypes/", methods =['GET', 'POST'])
def get_buildtypes():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT b.* "
    "FROM buildTypes b; ")
    data = cursor.fetchall()
    response = app.response_class(

        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

# Get center of gravity  types 
@app.route("/cgtypes/", methods =['GET', 'POST'])
def get_cgtypes():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT c.* "
    "FROM centerGravityTypes c; ")
    data = cursor.fetchall()
    response = app.response_class(

        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

# Get brake mode types 
@app.route("/brake/", methods =['GET', 'POST'])
def get_brakemodetypes():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT c.* "
    "FROM brakeModeTypes c; ")
    data = cursor.fetchall()
    response = app.response_class(

        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response
 
# Get Matches Data from past events
@app.route("/matches/", methods =['GET', 'POST'], defaults={'eventID':None})
@app.route("/matches/<eventID>")
def get_matches(eventID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if eventID is not None:
        cursor.execute("SELECT m.* "
                "FROM matches m, events e "
                "WHERE e.eventID = m.eventID "
                "AND e.eventID = " + eventID + ";")
    else:
        cursor.execute("SELECT m.* "
                "FROM matches m, events e "
                "WHERE e.eventID = m.eventID "
                "AND e.currentEvent = 1;")
    data = cursor.fetchall()	
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json' 
    )
    return response
    
# Get 195Data
@app.route("/195Data/", defaults={'team': None})
@app.route("/195Data/<team>")
def get_195Data(team):
    #args = request.args
    #team = args.get('team')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if team is not None:
        cursor.execute("SELECT m.* "
                "FROM MatchScouting m, Events e "
                "WHERE e.EventID = m.EventID "
                "AND Team="+team+" "
                "AND e.currentEvent = 1;")
    else: 
        cursor.execute("SELECT m.* "
                "FROM MatchScouting m, Events e "
                "WHERE e.EventID = m.EventID "
                "AND e.currentEvent = 1;")    
    data = cursor.fetchall()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


# Get Event Team List
@app.route("/currteam/", methods =['GET', 'POST'], defaults={'eventID' : None})
@app.route("/currteam/<eventID>")
def get_currteam(eventID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if eventID is not None:
        cursor.execute("SELECT t.team FROM teams t, events e "
                "WHERE t.eventID = e.eventID "
                "AND e.eventID = " + eventID +
                " order by cast(t.team as int);")
    else: 
        cursor.execute("SELECT t.team FROM teams t, events e "
                "WHERE t.eventID = e.eventID "
                "AND e.currentEvent = 1 "
                "order by cast(t.team as int);")
    data = cursor.fetchall()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

# Get Summary Data from past events 
@app.route("/summary/", methods =['GET', 'POST'], defaults={'eventID' : None})
@app.route("/summary/<eventID>")
def get_summary(eventID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if eventID is not None:
        cursor.execute("select a.* from CEanalysisGraphs a, events e "
                "where a.eventID=e.eventID "
                "and e.eventID = " + eventID + ";")
    else: 
        cursor.execute("select a.* from CEanalysisGraphs a, events e "
                    "where a.eventID=e.eventID "
                    "and e.currentEvent = 1;")
    data = cursor.fetchall()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


# Get Level1 Data
@app.route("/matchscouting/", methods =['GET', 'POST'], defaults={'allianceStationID': None})
@app.route("/matchscouting/<allianceStationID>")
def get_matchscouting(allianceStationID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if allianceStationID is not None:
        cursor.execute("select ms.*, m.blue1, m.blue2, m.blue3, m.red1, m.red2, m.red3, t.teamName "
                "FROM matchScouting ms, matches m, events e, teams t "
                "WHERE ms.matchID = m.matchID "
                "AND m.eventID = e.eventID "
                "AND e.currentEvent = 1 "
                "AND t.eventID = ms.eventID "
                "AND t.team = ms.team "
                "AND ms.scoutingStatus is NULL "
                "AND allianceStationID =" +allianceStationID+ ";")
    else: 
        cursor.execute("select ms.*, m.blue1, m.blue2, m.blue3, m.red1, m.red2, m.red3, t.teamName "
                "FROM matchScouting ms, matches m, events e, teams t "
                "WHERE ms.matchID = m.matchID "
                "AND m.eventID = e.eventID "
                "AND e.currentEvent = 1 "
                "AND t.eventID = ms.eventID "
                "AND t.team = ms.team "
                "AND ms.scoutingStatus = 2;")
    data = cursor.fetchall()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

# Get Analysis Data from past events
@app.route("/analysis195/", methods =['GET', 'POST'], defaults = {'eventID': None})
@app.route("/analysis195/<eventID>")
def get_analysis(eventID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if eventID is not None:
        cursor.execute("SELECT cea.*, at.analysisType "
                "FROM CEanalysis cea, analysisTypes at "
                "WHERE cea.eventID = " + eventID + " "
                "AND cea.analysisTypeID = at.analysisTypeID order by cea.analysisTypeID;")
    else:
        cursor.execute("SELECT cea.*, at.analysisType "
                "FROM CEanalysis cea, analysisTypes at, events e "
                "WHERE cea.eventID = e.eventID "
                "AND e.currentEvent = 1 "
                "AND cea.analysisTypeID = at.analysisTypeID order by analysisTypeID;")
    data = cursor.fetchall()	
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

# Get Matches Info from past events 
@app.route("/matchinfo/", methods =['GET', 'POST'], defaults = {'eventID' : None})
@app.route("/matchinfo/<eventID>")
def get_matchinfo(eventID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if eventID is not None:
        cursor.execute("SELECT m.* "
                    "FROM matches m, events e "
                    "WHERE e.eventID = m.eventID "
                    "and e.eventID = " + eventID + " ORDER BY m.matchNum;")
    else:
        cursor.execute("SELECT m.* "
                "FROM matches m, events e "
                "WHERE e.eventID = m.eventID "
                "AND e.currentEvent = 1 ORDER BY m.matchNum;")
    data = cursor.fetchall()	
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json' 
    )
    return response


# Get Pit Data
@app.route("/pitdata/", methods =['GET', 'POST'], defaults = {'eventID' : None})
@app.route("/pitdata/<eventID>")
def get_pitdata(eventID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if eventID is not None:
        cursor.execute("SELECT p.*, d.driveBaseType, t.teamName, teamLocation, m.driveMotorType, a.manipulatorType, "
            "s.superClimbType, b.buildType, c.centerGravityType, bm.brakeModeType "
                "FROM pit p "
                "INNER JOIN teams t on p.team = t.team AND p.eventID = t.eventID "
                "INNER JOIN events e on p.eventID = e.eventID "
                "LEFT JOIN driveBaseTypes d on p.driveBaseTypeID=d.driveBaseTypeID "
                "LEFT JOIN driveMotorTypes m on p.driveMotorTypeID=m.driveMotorTypeID "
                "LEFT JOIN manipulatorTypes a on p.manipulatorTypeID=a.manipulatorTypeID "
                "LEFT JOIN superClimbTypes s on p.superClimbTypeID=s.superClimbTypeID "
                "LEFT JOIN buildTypes b on p.buildTypeID=b.buildTypeID "
                "LEFT JOIN brakeModeTypes bm on p.brakeModeTypeID=bm.brakeModeTypeID "
                "LEFT JOIN centerGravityTypes c on p.centerGravityTypeID=c.centerGravityTypeID "
                "WHERE p.eventID = " + eventID + " ;")
    else: 
        cursor.execute("SELECT p.*, d.driveBaseType, t.teamName, teamLocation, m.driveMotorType, a.manipulatorType, "
            "s.superClimbType, b.buildType, c.centerGravityType, bm.brakeModeType "
                "FROM pit p "
                "INNER JOIN teams t on p.team = t.team AND p.eventID = t.eventID "
                "INNER JOIN events e on p.eventID = e.eventID "
                "LEFT JOIN driveBaseTypes d on p.driveBaseTypeID=d.driveBaseTypeID "
                "LEFT JOIN driveMotorTypes m on p.driveMotorTypeID=m.driveMotorTypeID "
                "LEFT JOIN manipulatorTypes a on p.manipulatorTypeID=a.manipulatorTypeID "
                "LEFT JOIN superClimbTypes s on p.superClimbTypeID=s.superClimbTypeID "
                "LEFT JOIN buildTypes b on p.buildTypeID=b.buildTypeID "
                "LEFT JOIN brakeModeTypes bm on p.brakeModeTypeID=bm.brakeModeTypeID "
                "LEFT JOIN centerGravityTypes c on p.centerGravityTypeID=c.centerGravityTypeID "
                "WHERE p.eventID = e.eventID "
                "AND e.currentEvent = 1 ;") 
    data = cursor.fetchall()
    response = app.response_class(

        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


#get pit scouting data from past events
@app.route("/pitscouting/", methods =['GET', 'POST'], defaults = {'eventID': None})
@app.route("/pitscouting/<eventID>")
def get_pitscouting(eventID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if eventID is not None:   
        cursor.execute("select p.*, t.teamName "
                "from pit p, events e, teams t "
                "where e.eventID = " + eventID + " "
                "AND p.eventID = e.eventID "
                "and t.eventID = p.eventID "
                "AND t.team = p.team;") 
    else: 
        cursor.execute("select p.*, t.teamName "
                "from pit p, events e, teams t "
                "where e.currentEvent = 1 "
                "AND p.eventID = e.eventID "
                "and t.eventID = p.eventID "
                "AND t.team = p.team;") 
    data = cursor.fetchall()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

    # Get Level2 Data
@app.route("/matchscoutingl2/", methods =['GET', 'POST'], defaults={'allianceStationID': None})
@app.route("/matchscoutingl2/<allianceStationID>")
def get_matchscoutingl2(allianceStationID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if allianceStationID is not None:
        cursor.execute("select ms.*, m.blue1, m.blue2, m.blue3, m.red1, m.red2, m.red3, t.teamName "
                "from matchScoutingL2 ms, matches m, events e, teams t "
                "where ms.matchID = m.matchID "
                "AND m.eventID = e.eventID "
                "AND e.currentEvent = 1 "
                "AND t.eventID = ms.eventID "
                "AND t.team = ms.team " 
                "AND ms.scoutingStatus is NULL "
                "and allianceStationID =" +allianceStationID+ ";")
    else: 
       
        cursor.execute("select ms.*, m.blue1, m.blue2, m.blue3, m.red1, m.red2, m.red3, t.teamName "
                "from matchScoutingL2 ms, matches m, events e, teams t "
                "where ms.matchID = m.matchID "
                "AND m.eventID = e.eventID "
                "AND e.currentEvent = 1 "
                "AND t.eventID = ms.eventID "
                "AND t.team = ms.team "
                "AND ms.scoutingStatus is NULL;")
    
    data = cursor.fetchall()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


# Get Matches Info from past events 
@app.route("/checklist/", methods =['GET', 'POST'], defaults = {'eventID' : None})
@app.route("/checklist/<eventID>")
def get_checklist(eventID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if eventID is not None:
        cursor.execute("SELECT c.*, t.task, t.taskDesc "
                    "FROM checklist c, tasks t, events e "
                    "WHERE c.taskID = t.taskID " 
                    "and e.eventID = c.eventID "
                    "and e.eventID = " + eventID + " ORDER BY c.matchNum;")
    else:
        cursor.execute("SELECT c.*, t.task, t.taskDesc "
                    "FROM checklist c, tasks t, events e "
                    "WHERE c.taskID = t.taskID " 
                    "and e.eventID = c.eventID "
                    "AND e.currentEvent = 1 ORDER BY c.matchNum;")
    data = cursor.fetchall()	
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json' 
    )
    return response




# Get Analysis Type Data
@app.route("/types/", methods =['GET', 'POST'])
def get_types():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT analysisTypeID, analysisType, teamPicker, matchReport, "
                   "robotSnapshot, developer, summary, sortOrder from analysisTypes;")
    data = cursor.fetchall()	
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


# Get level 2 Data
@app.route("/level2/", methods =['GET', 'POST'], defaults = {'eventID': None})
@app.route("/level2/<eventID>")
def get_level2(eventID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if eventID is not None:   
        cursor.execute("select a.matchNum, a.team, a.commentOff, a.commentDef, a.goodOffBot, a.goodDefBot "
                "from matchScoutingL2 a, events e "
                "where a.eventID=e.eventID "
                "and e.eventID = " + eventID + " "
                "and a.scoutingStatus = 1 "
                "order by matchNum;")
    else: 
        cursor.execute("select a.matchNum, a.team, a.commentOff, a.commentDef, a.goodOffBot, a.goodDefBot "
                "from matchScoutingL2 a, events e "
                "where a.eventID=e.eventID "
                "and e.currentEvent = 1 "
                "and a.scoutingStatus = 1 "
                "order by matchNum;")
    data = cursor.fetchall()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


# Get Final 24 Data
@app.route("/final24Old", methods =['GET'])
def get_final24Old():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * from final24;")
    data = cursor.fetchall()	
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


# Update FInal24 Data
@app.route("/final24-update", methods =['POST'])
def post_final24():
    # TODO: IMPLEMENT ME

    if not request.is_json:
        return Response('Invalid submission, please submit as JSON.', status=400)
    data = request.json

    for line in data:
        print(line)
    
    table = request.args.get('table', default = '*', type = str)

    print("Updating " + table + " table")

    # SortOrder is gone from the frontend code - you'll need to iterate through
    # the rows and get SortOrder from the position of the row. Something like

    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
        for pos, team_selection in enumerate(data):
            #cursor.execute('UPDATE Final24 SET Team =% s where SortOrder=%s', (team_selection['Team'],pos+1))
            #query1='INSERT INTO '+table+' VALUES (%s, %s) ON DUPLICATE KEY UPDATE Team=%s',(pos+1, team_selection['Team'],team_selection['Team'])
            ##print(query1)
            #cursor.execute(query1)
            cursor.execute('INSERT INTO '+table+' VALUES (%s, %s) ON DUPLICATE KEY UPDATE team=%s',(pos+1, team_selection['team'],team_selection['team']))
        mysql.connection.commit()

    return '1'





# Update Pit Scouting Data
@app.route("/pit-update", methods =['POST'])
def post_pitscouting():

    if not request.is_json:
        return Response('Invalid submission, please submit as JSON.', status=400)
    data = request.json

    for line in data:
        print(line)

    # SortOrder is gone from the frontend code - you'll need to iterate through
    # the rows and get SortOrder from the position of the row. Something like

    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
        for pos, pit_data in enumerate(data):
            #cursor.execute('UPDATE Final24 SET Team =% s where SortOrder=%s', (team_selection['Team'],pos+1))
            #query1='INSERT INTO '+table+' VALUES (%s, %s) ON DUPLICATE KEY UPDATE Team=%s',(pos+1, team_selection['Team'],team_selection['Team'])
            ##print(query1)
            #cursor.execute(query1)
            cursor.execute('UPDATE pit SET buildComments = %s, buildQuality = %s, buildTypeID = %s, centerGravityTypeID = %s, brakeModeTypeID = %s, '
                'driveBaseTypeID = %s, driveMotorTypeID = %s, electricalComments= %s, electricalQuality = %s, '
                'generalComments = %s, imageLink = %s, manipulatorTypeID = %s, robotDurability = %s, robotHeight = %s, '
                'robotLength = %s, robotWidth = %s, scouterID = %s, scoutingStatus = %s, superClimbTypeID = %s, robotWeight = %s '
                'where team = %s and eventID = %s',(pit_data['buildComments'],pit_data['buildQuality'],pit_data['buildTypeID'],pit_data['centerGravityTypeID'],pit_data['brakeModeTypeID'],
                pit_data['driveBaseTypeID'],pit_data['driveMotorTypeID'],pit_data['electricalComments'],pit_data['electricalQuality'],
                pit_data['generalComments'],pit_data['imageLink'],pit_data['manipulatorTypeID'],pit_data['robotDurability'],pit_data['robotHeight'],
                pit_data['robotLength'],pit_data['robotWidth'],pit_data['scouterID'],pit_data['scoutingStatus'],pit_data['superClimbTypeID'],pit_data['robotWeight'],
                pit_data['team'],pit_data['eventID']))
        mysql.connection.commit()

    return '1'


# Update Pit Scouting Status
@app.route("/pit-status", methods =['POST'])
def post_pitscouting2():
    # TODO: IMPLEMENT ME

    if not request.is_json:
        return Response('Invalid submission, please submit as JSON.', status=400)
    data = request.json

    for line in data:
        print(line)

    # SortOrder is gone from the frontend code - you'll need to iterate through
    # the rows and get SortOrder from the position of the row. Something like

    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
        for pos, pit_data in enumerate(data):
            #cursor.execute('UPDATE Final24 SET Team =% s where SortOrder=%s', (team_selection['Team'],pos+1))
            #query1='INSERT INTO '+table+' VALUES (%s, %s) ON DUPLICATE KEY UPDATE Team=%s',(pos+1, team_selection['Team'],team_selection['Team'])
            ##print(query1)
            #cursor.execute(query1)
            cursor.execute('UPDATE pit SET scoutingStatus = %s where team = %s and eventID = %s',(pit_data['scoutingStatus'],pit_data['team'],pit_data['eventID']))
        mysql.connection.commit()

    return '1'



    
# Update Pit Scouting Data
@app.route("/level2-update", methods =['POST'])
def post_level2sccouting():

    if not request.is_json:
        return Response('Invalid submission, please submit as JSON.', status=400)
    data = request.json

    for line in data:
        print(line)

    # SortOrder is gone from the frontend code - you'll need to iterate through
    # the rows and get SortOrder from the position of the row. Something like

    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
        for pos, lvl2_data in enumerate(data):
            #cursor.execute('UPDATE Final24 SET Team =% s where SortOrder=%s', (team_selection['Team'],pos+1))
            #query1='INSERT INTO '+table+' VALUES (%s, %s) ON DUPLICATE KEY UPDATE Team=%s',(pos+1, team_selection['Team'],team_selection['Team'])
            ##print(query1)
            #cursor.execute(query1)
            cursor.execute('UPDATE matchScoutingL2 SET speed = %s, maneuverability = %s, sturdiness = %s, climb = %s, '
                'effort = %s, scoringEff = %s, intakeEff = %s, commentOff= %s, commentDef = %s, goodOffBot = %s, goodDefBot = %s, '
                'scouterID = %s, scoutingStatus = %s, defCommunity = %s, defCenter = %s, defLZ = %s, preNoShow = %s '
                'where matchScoutingL2ID = %s and (scoutingStatus not in (1,3) or scoutingStatus is null)',(lvl2_data['speed'],lvl2_data['maneuverability'],lvl2_data['sturdiness'],lvl2_data['climb'],
                lvl2_data['effort'],lvl2_data['scoringEff'],lvl2_data['intakeEff'],lvl2_data['commentOff'],lvl2_data['commentDef'],
                lvl2_data['goodOffBot'],lvl2_data['goodDefBot'],lvl2_data['scouterID'],lvl2_data['scoutingStatus'],lvl2_data['defCommunity'],lvl2_data['defCenter'],lvl2_data['defLZ'],
                lvl2_data['preNoShow'],lvl2_data['matchScoutingL2ID']))
            
        mysql.connection.commit()

    return '1'
        
# Update Pit Scouting Data
@app.route("/level1-update", methods =['POST'])
def post_level1sccouting():
    # TODO: IMPLEMENT ME

    if not request.is_json:
        return Response('Invalid submission, please submit as JSON.', status=400)
    data = request.json

    for line in data:
        print(line)

    # SortOrder is gone from the frontend code - you'll need to iterate through
    # the rows and get SortOrder from the position of the row. Something like

    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
        for pos, lvl1_data in enumerate(data):
            #cursor.execute('UPDATE Final24 SET Team =% s where SortOrder=%s', (team_selection['Team'],pos+1))
            #query1='INSERT INTO '+table+' VALUES (%s, %s) ON DUPLICATE KEY UPDATE Team=%s',(pos+1, team_selection['Team'],team_selection['Team'])
            ##print(query1)
            #cursor.execute(query1)
            cursor.execute('UPDATE matchScouting SET preStartPos = %s, preLoad = %s, preNoShow = %s, autoMB = %s, autoRamp = %s, autoPen = %s, '
                'autoScore1 = %s, autoScore2 = %s, scouterID = %s, scoutingStatus = %s, autoScore3 = %s, autoScore4 = %s, teleConeHigh = %s, '
                'teleCubeHigh = %s, teleConeMid = %s, teleCubeMid = %s, teleConeLow = %s, teleCubeLow = %s, teleConeCMTY = %s, teleCubeCMTY = %s, teleLZPickup = %s,'
                'teleObstructed = %s, teleWasObstructed = %s, ramp = %s, rampAssist = %s, rampPos = %s, rampStartTime = %s, postSubsystemBroke = %s, '
                'postBrokeDown = %s, postReorientCone = %s, postShelfPickup = %s, postGroundPickup = %s, postGoodPartner = %s, postTippedOver = %s '
                'where matchScoutingID = %s and (scoutingStatus not in (1,3) or scoutingStatus is null)' ,(lvl1_data['preStartPos'],lvl1_data['preLoad'],lvl1_data['preNoShow'],lvl1_data['autoMB'],lvl1_data['autoRamp'],lvl1_data['autoPen'],
                lvl1_data['autoScore1'],lvl1_data['autoScore2'],lvl1_data['scouterID'],lvl1_data['scoutingStatus'],lvl1_data['autoScore3'],lvl1_data['autoScore4'],lvl1_data['teleConeHigh'],
                lvl1_data['teleCubeHigh'],lvl1_data['teleConeMid'],lvl1_data['teleCubeMid'],lvl1_data['teleConeLow'],lvl1_data['teleCubeLow'],lvl1_data['teleConeCMTY'],lvl1_data['teleCubeCMTY'],lvl1_data['teleLZPickup'],
                lvl1_data['teleObstructed'],lvl1_data['teleWasObstructed'],lvl1_data['ramp'],lvl1_data['rampAssist'],lvl1_data['rampPos'],lvl1_data['rampStartTime'], lvl1_data['postSubsystemBroke'],
                lvl1_data['postBrokeDown'],lvl1_data['postReorientCone'],lvl1_data['postShelfPickup'],lvl1_data['postGroundPickup'],lvl1_data['postGoodPartner'],
                lvl1_data['postTippedOver'],lvl1_data['matchScoutingID']))
            
        mysql.connection.commit()

    return '1'


# Delete Final24 Data
@app.route("/final24", methods =['DELETE'])
def delete_final24():
    # TODO: IMPLEMENT ME

    #if not request.is_json:
    #    return Response('Invalid submission, please submit as JSON.', status=400)
    #data = request.json

    # Would like to loop through JSON file and delete rows on the database.
    # Just need to figure out how to read the JSON file.
    print("*******Deleting Records*********")
    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
      
        cursor.execute('DELETE from Final24 where SortOrder > 0')
        mysql.connection.commit()

    return '1'

# Get DNP List Data
@app.route("/dnp", methods =['GET'])
def get_dnp():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * from DnpList;")
    data = cursor.fetchall()	
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

# Update FInal24 Data
@app.route("/dnp-update", methods =['POST'])
def post_dnp():

    if not request.is_json:
        return Response('Invalid submission, please submit as JSON.', status=400)
    data = request.json

    for line in data:
        print(line)

    # SortOrder is gone from the frontend code - you'll need to iterate through
    # the rows and get SortOrder from the position of the row. Something like

    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
        for pos, team_selection in enumerate(data):
            #cursor.execute('UPDATE Final24 SET Team =% s where SortOrder=%s', (team_selection['Team'],pos+1))
            cursor.execute('INSERT INTO DnpList VALUES (%s, %s) ON DUPLICATE KEY UPDATE Team=%s',(pos+1, team_selection['Team'],team_selection['Team']))
        mysql.connection.commit()

    return '1'

# Get DNP List Data
@app.route("/pick", methods =['GET'])
def get_pick():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * from pickList1;")
    data = cursor.fetchall()	
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

# Get List Data
@app.route("/final24", methods =['GET'])
def get_final24():

    table = request.args.get('table', default = '*', type = str)

    print("Retrieve data from " + table + " table")

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * from "+table+";")
    data = cursor.fetchall()	
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


# Validate User Credentials
@app.route("/access", methods =['GET'])
def get_user():
    print("Validating Login")

    userName = request.args.get('userName', default = '*', type = str)
    userPass = request.args.get('userPass', default = '*', type = str)
    # userName = request.args.get('userName', default = '*', type = str)

    print("userName: [" + userName + "]")
    print("userPass: [" + userPass + "]")

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("select analysisAccess, scoutingAccess from users "
            "where userName = '" + userName + "' "
            "and userPass = '" + userPass + "';" )
    data = cursor.fetchall()	
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    print(response)
    return response


# def get_currteam():
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("SELECT t.team "
#                 "FROM teams t, events e "
#                 "WHERE t.eventID = e.eventID "
#                 "AND e.currentEvent = 1 "
#                 "order by cast(t.team as int);")
#     data = cursor.fetchall()
#     response = app.response_class(
#         response=json.dumps(data),
#         status=200,
#         mimetype='application/json'
#     )
#     return response




@app.route('/upload/<team>', methods=['GET','POST'])
def upload_file(team):

    file = request.files['robotImage']

    print("File Upload: [" + team + "] [" + str(file) +"]")

    # print("Old File: " + file.filename)

    filepart = os.path.splitext(file.filename)
    extension = filepart[1]
    filename = "frc" + team + extension
    # print("New File: " + filename)

    filename = secure_filename(filename)

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
    return '0'

@app.route('/image/', methods=['GET','POST'])
def get_list():

    path = UPLOAD_FOLDER

    # Return 404 if path doesn't exist
    if not os.path.exists(path):
        return '404'
    
    # Show directory contents
    files = os.listdir(path)

    response = app.response_class(
        response=json.dumps(files),
        status=200,
        mimetype='application/json'
    )

    print(response)

    return response


# Update Checklist Data
@app.route("/checklist-update", methods =['POST'])
def post_checklist_update():

    if not request.is_json:
        return Response('Invalid submission, please submit as JSON.', status=400)
    data = request.json

    for line in data:
        print(line)

    # SortOrder is gone from the frontend code - you'll need to iterate through
    # the rows and get SortOrder from the position of the row. Something like

    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
        for pos, list_data in enumerate(data):
            #cursor.execute('UPDATE Final24 SET Team =% s where SortOrder=%s', (team_selection['Team'],pos+1))
            #query1='INSERT INTO '+table+' VALUES (%s, %s) ON DUPLICATE KEY UPDATE Team=%s',(pos+1, team_selection['Team'],team_selection['Team'])
            ##print(query1)
            #cursor.execute(query1)
            cursor.execute('UPDATE checklist SET taskStatus = %s where listID = %s',(list_data['taskStatus'],list_data['listID']))
            
        mysql.connection.commit()

    return '1'




if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)

