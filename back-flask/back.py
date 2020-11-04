from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import pickle
import ast
app = Flask(__name__)
CORS(app)
data = pd.read_csv("df.csv")
states = {"CA": "CALIFORNIA",
          "TX": "TEXAS",
          "FL": "FLORIDA",
          "CO": "COLORADO",
          "AZ": "ARIZONA",
          "NC": "NORTH CAROLINA",
          "IL": "ILLINOIS",
          "WA": "WASHINGTON",
          "GA": "GEORGIA",
          "MI": "MICHIGAN",
          "NJ": "NEW JERSEY",
          "VA": "VIRGINIA",
          "OH": "OHIO",
          "TN": "TENNESSEE",
          "AL": "ALABAMA",
          "CT": "CONNECTICUT",
          "KS": "KANSAS",
          "MA": "MASSACHUSETTS",
          "MO": "MISSOURI",
          "NV": "NEVADA",
          "NY": "NEW YORK",
          "OR": "OREGON",
          "IN": "INDIANA",
          "LA": "LOUISIANA",
          "OK": "OKLAHOMA",
          "UT": "UTAH",
          "WI": "WISCONSIN",
          "IA": "IOWA",
          "MN": "MINNESOTA",
          "PA": "PENNSYLVANIA",
          "SC": "SOUTH CAROLINA",
          "ID": "IDAHO",
          "KY": "KENTUCHY",
          "NE": "NEBRASKA",
          "NM": "NEW MEXICO",
          "AK": "ALASKA",
          "AR": "ARKANSAS",
          "DC": "DISTRICT OF COLUMBIA",
          "HI": "HAWAII",
          "MD": "MARYLAND",
          "MS": "MISSISSIPPI",
          "MT": "MONTANA",
          "ND": "NORTH DAKOTA",
          "NH": "NEW HAMPSHIRE",
          "RI": "RHODE ISLAND",
          "SD": "SOUTH DAKOTA",
          "DE": "DELAWARE",
          "ME": "MAINE",
          "VT": "VERMONT",
          "WV": "WEST VIRGINIA",
          "WY": "WYOMING"}


@app.route('/topTechnologies/', methods=['GET'])
def getTop5():
    def count_frequencies(row):
        technologies = ast.literal_eval(row["technologies"])
        for technology in technologies:
            ind = final_technologies.index(technology)
            technologies_frequencies[ind] = technologies_frequencies[ind]+1
    final_technologies = pickle.load(open('final_technologies.pickle', 'rb'))
    technologies_frequencies = [0]*len(final_technologies)
    data.apply(count_frequencies, axis=1)
    top5 = []
    for i in range(5):
        ind = technologies_frequencies.index(max(technologies_frequencies))
        top5.append(final_technologies[ind])
        technologies_frequencies[ind] = 0
    return jsonify(top5)

# For BarChart ( yaxis )
@app.route('/nbTechnologies/', methods=['GET'])
def getNbTechnologies():
    def count_frequencies(row):
        technologies = ast.literal_eval(row["technologies"])
        for technology in technologies:
            ind = final_technologies.index(technology)
            technologies_frequencies[ind] = technologies_frequencies[ind]+1
    final_technologies = pickle.load(open('final_technologies.pickle', 'rb'))
    technologies_frequencies = [0]*len(final_technologies)
    data.apply(count_frequencies, axis=1)
    top5 = []
    for i in range(5):
        ind = technologies_frequencies.index(max(technologies_frequencies))
        top5.append(final_technologies[ind])
        technologies_frequencies[ind] = 0

    def countJobs(row):
        for technology in top5:
            if(technology in row["technologies"]):
                ind = top5.index(technology)
                nbJobs[ind] = nbJobs[ind]+1
    nbJobs = [0, 0, 0, 0, 0]
    data.apply(countJobs, axis=1)
    return jsonify(nbJobs)

# For PieChart
@app.route('/TechnologiesPerTrack/', methods=['GET'])
def TechnologiesPerTrack():
    def countTechnologies(row):
        for track in tracks:
            if(row[track] == 1):
                ind = tracks.index(track)
                technologies = ast.literal_eval(row["technologies"])
                for technology in technologies:
                    tracks_technologies[ind].add(technology)
    nbTechnologies = [0, 0, 0, 0, 0]
    tracks_technologies = [set(), set(), set(), set(), set()]
    tracks = ['ds', 'web_development', 'devops', 'mobile', 'cyber_security']
    data.apply(countTechnologies, axis=1)
    for n in range(5):
        nbTechnologies[n] = len(tracks_technologies[n])
    return jsonify(nbTechnologies)

# For LineChart ( yaxis )
@app.route('/JobsPerDates/', methods=['GET'])
def Technologies():
    def get_dates(row):
        dates.add(row["posted_date"])

    def count_frequencies(row):
        technologies = ast.literal_eval(row["technologies"])
        for technology in technologies:
            ind = final_technologies.index(technology)
            technologies_frequencies[ind] = technologies_frequencies[ind]+1

    def count_jobPerDate(row):
        date = row["posted_date"]
        if (date in dates):
            technologies = ast.literal_eval(row["technologies"])
            for technology in top5:
                if technology in technologies:
                    ind1 = dates.index(date)
                    ind2 = top5.index(technology)
                    values[ind2][ind1] = values[ind2][ind1]+1
    final_technologies = pickle.load(open('final_technologies.pickle', 'rb'))
    technologies_frequencies = [0]*len(final_technologies)
    data.apply(count_frequencies, axis=1)
    top5 = []
    for i in range(5):
        ind = technologies_frequencies.index(max(technologies_frequencies))
        top5.append(final_technologies[ind])
        technologies_frequencies[ind] = 0
    dates = set()
    data.apply(get_dates, axis=1)
    dates = list(dates)
    # dates=dates[0:30]
    values = [[0]*len(dates), [0]*len(dates), [0]*len(dates), [0]*len(dates),
              [0]*len(dates)]
    data.apply(count_jobPerDate, axis=1)
    return jsonify({"values": values, "dates": dates})

# For BarChart for States
@app.route('/statesTechnologies/', methods=['GET'])
def statesTechnologies():
    def count_states_technologies(row):
        state = row["state"]
        if not(pd.isnull(state)):
            ind = names.index(state)
            technologies = ast.literal_eval(row["technologies"])
            for technology in technologies:
                states_technologies[ind].add(technology)
    names = list(states.values())
    states_technologies = []
    for n in range(len(names)):
        states_technologies.append(set())
    values = [0]*len(names)
    data.apply(count_states_technologies, axis=1)
    for n in range(len(names)):
        values[n] = len(states_technologies[n])
    return jsonify(values)

# For PieChart when BarChart clicked
@app.route('/technologyDistribution/', methods=['POST'])
def technologyDistributionPerState():
    def count(row):
        for track in tracks:
            if(row[track] == 1):
                technologies = ast.literal_eval(row["technologies"])
                if (technology in technologies):
                    ind = tracks.index(track)
                    distribution_of_technology[ind] =\
                        distribution_of_technology[ind]+1
    technology = request.get_json(force=True).get('technology')
    tracks = ['ds', 'web_development', 'devops', 'mobile', 'cyber_security']
    distribution_of_technology = [0, 0, 0, 0, 0]
    data.apply(count, axis=1)
    return jsonify(distribution_of_technology)

# For BarChart for States when BarChart clicked
@app.route('/technologyDistributionPerState/', methods=['POST'])
def technologyDistribution():
    def count(row):
        state = row["state"]
        if not(pd.isnull(state)):
            ind = names.index(state)
            technologies = ast.literal_eval(row["technologies"])
            if (technology in technologies):
                values[ind] = values[ind]+1
    technology = request.get_json(force=True).get('technology')
    names = list(states.values())
    values = [0]*len(names)
    data.apply(count, axis=1)
    return jsonify(values)


if __name__ == '__main__':
    app.run(debug=True)
