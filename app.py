from flask import Flask, render_template
import random
app = Flask(__name__)
app.config['SECRET_KEY'] = 'zslzslzsl'


@app.route("/")
def root():
    """
    :return: Index.html
    """
    return render_template('Index.html')


@app.route('/api/recommend')
def get_tasks():
    # todo:receive data from db or UI input?
    my_list = ['z', 'x', 'f', 'l', 'g', 'c' ,'c','f','f','g']
    return recommend_activity(my_list)


def recommend_activity(activities):
    dict = {}
    for x in activities:
        if x in dict:
            dict[x] += 1
        else:
            dict[x] = 1
    res = sorted(dict, key=lambda x: (-dict[x], x))
    if len(res) >= 2 and dict[res[0]] == dict[res[-1]]:
        return 'The distribution of votes is too even, so a popular activity is recommended randomly: '+random_recommendation()
    else:
        return 'The activities with the highest voting results is: '+" ".join(str(i) for i in res[:4])


def random_recommendation():
    list_random = ['act1','act2','act3','act4','act5','act6']
    res = random.choices(list_random, k=4)
    return " ".join(str(i) for i in res)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='5000')
