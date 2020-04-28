from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from githubclient import api

with app.app_context():
    __api_instance = api.Api()

@app.route('/')
def welcome_to_github_client():
    return """
        Welcome to github client!
        <br/>
        <br/>
        This application has two endpoints:
        <br/>
        <br/>
        1. active/{user} <br/>
        2. downwards/{owner}/{repository} 
        <br/><br/>
        The first endpoint shows, how active the user is. <br/>
        The endpoint returns JSON response with boolean 'isActive' field.<br/>
        If the user has pushed the code to any repository in the last 24 hours,
        the field will have the value true or false, depending on the results of user's activity. 
        <br/><br/>
        {user} parameter denotes username of the person on github. <br/>
        {owner} is the same as the <user> parameter, but in the second endpoint it means, 
        that the user owns the repository.<br/>
        {repository} is the name of the repository, it could be found at user's page on github.
        <br/><br/>
        The second endpoint shows, whether the amount of the code has been reduced in the repository.<br/>
        The endpoint returns JSON response with boolean field 'isDownwards'.<br/>
        If there were more additions, than deletions in the last 7 days, then this field will be set to true. <br/>
        In other scenario this field will be set to false.
        <br/><br/>
        !This app is able to query only PUBLIC github repositories. The private repositories and events 
        will not be taken into account!
        <br/><br/>
        If something goes wrong, the app will tell you about that.<br/>
        Enjoy!<br/><br/>
    """

"""

'Active' endpoint.
If the user pushed to any repository in the last 24 hours, then the 'True' returned in result.
Otherwise, 'False' will be returned.
The result is returned as json response with 'isActive' boolean field.
In case of unexpected behaviour the json with single 'error_message' field is returned.
"""

@app.route('/active/<user>', methods=['GET'])
def active(user):
    try:
        return dict(isActive=__api_instance.active(user))
    except Exception as ex:
        return dict(error_message=('Oops! Something went wrong. Please, try again. Exception message: <br></br> '
                                   + str(ex))
                    )

"""

'Downwards' endpoint.

If there were more deletions than additions of code in the given repository, then 'True' will be returned.
Otherwise 'false' will be returned.
The result is returned as json response with 'downwards' boolean field.

In case of unexpected behaviour the json with single 'error_message' field is returned.

"""
@app.route('/downwards/<owner>/<repository>', methods=['GET'])
def downwards(owner, repository):
    try:
        return dict(downwards=__api_instance.downwards(owner, repository))
    except Exception as ex:
        return dict(error_message=('Oops! Something went wrong. Please, try again. Exception message: <br></br> '
                                   + str(ex))
                    )


@app.route('/healthz', methods=['GET'])
def healthz():
    return {"status": "OK"}


print("Starting the github client...")
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0')
    finally:
        from githubclient.pool_holder import PoolHolder

        PoolHolder.instance().close()
