# SQLAlchemy Challenge
> How can we both answer questions by manipulating data and release those answers onto the internet for other people to use at the same time?
## Folder Contents
- A `Resource` folder containing all the data used for this project.
  - `hawaii_stations.csv` contains a table of stations collecting Honolulu's weather data.
  - `hawaii_measurements.csv` contains a table of climate measurements the aforementioned stations collected over a period of time.
  - `hawaii.sqlite` creates schemas and imports the CSV files above into manageable tables to be used for later analysis. Database management systems or administrators not required.
- A `Climate Data Analysis.ipynb` Notebook file that does basic exploratory data analysis with the files in the `Resource` folder.
- An `app.py` Python file serving as an API system using the files in the `Resources` folder in order to provide answers to simple GET requests.
  - To be run in a terminal or whatever console that can run Python code - I used Anaconda Prompt and ran it in my development environment with all its dependencies active.
  - Upon running the program, you should, by default, be able to input `http://127.0.0.1:5000/` or `localhost:5000/` into your browser's URL to test out the homemade API for yourself.
    ![What the API should look like and where you can find it](https://cdn.discordapp.com/attachments/939673945240637450/1130785584772825188/image.png)
- A .gitignore file that ignores common things like PyCache, Jupyter Notebook checkpoints, and other common gitignorable Python entities. 

### Installation/Prerequisites
- Make sure you can run Python. The development environment I used was set-up with:
```
conda create -n dev python=3.10 anaconda -y
```
#### Imported Modules
- Installing via the conda command given should give you access to most, if not all, of the script's modules locally. However, if you don't have them, be sure to grab yourself the following libraries:
  - [Pandas](https://pandas.pydata.org/docs/getting_started/install.html), [NumPy](https://numpy.org/install/), and [MatPlotLib](https://matplotlib.org/stable/users/installing/index.html), for your basic dataframe and graphical manipulation.
  - [SQLAlchemy](https://docs.sqlalchemy.org/en/20/intro.html#installation) for handling SQL data through Python.
  - [Flask](https://flask.palletsprojects.com/en/2.3.x/installation/) for creating applications that can be hosted on a computer or server.

## Code Breakdown
Similar to some of the previous exercises, this project is more of a proof of concept to familiarize us with working with Object Relational Mapping and creating our own APIs. The industry standard from the Python side of things when it comes to application development is probably Django, but, like Flask, it's also a web framework so many skills and concepts are transferrable.

Frankly, with some of the graphs such as this one here:
![One of the graphs generated in this project](https://cdn.discordapp.com/attachments/939673945240637450/1130795539622015016/image.png)

One might be tempted to say to just use Pandas and get the same results with a familiar coding framework. However, not everyone follows the same standards or languages. Companies and data departments might have prioritized storing information in SQL for heir faster queries, so it's not on us to decide where our data comes from.

### Main Takeaways
Examples of basic setup can be found here in the [official documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#basic-use). Generally, after setting up your schemas, your main operative code would work like this:
```python
# Run the session
session = Session(engine)

# Get data from database
results = session.query(Table.column1, Table.columnN).filter(Table.some_column >= some condition)

# Bring the data into a framework with more functions to work with, such as Pandas
results_df = pd.read_sql(results.statement, con = engine)

# Do stuff

# Like how you wouldn't leave air conditioning on in a room you won't use, close your sessions once you're done
session.close()
```

Similarly, in Flask, API calls are designed like so:
```python
# Define some route
@app.route("/some_route/<some_parameter>")
def some_function(some_parameter):
  # Run the session
  session = Session(engine)

  # Get data
  results = session.query(Something.here).all()

  # Close any open sessions
  session.close()

  # Do stuff to the data and/or process it into JSON responses by iterating through each row of results
  # Be sure to export the results as dictionaries -> JSON objects
  list = []
  for field1, field2, field3 in results:
    dict = {}
    dict["field1"] = field1
    dict["field2"] = field2
    dict["field3"] = field3
    list.append(dict)
  return jsonify(list) 
```

The rest of the optimization and manipulation is through experience and plenty of visits to Youtube and StackOverflow. Furthermore, as this is a web framework, you can also use whatever HTML/CSS/JS knowledge you have to spruce things up on your application. Once you get the hang of it, however, you can easily get neat results such as this image below and feel empowered by your gradual progress towards becoming a passable programmer.
![Sample cool API JSON response](https://cdn.discordapp.com/attachments/939673945240637450/1130802271253450762/image.png)

## Resources that helped a lot
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html) and [Flask Documentation](https://flask.palletsprojects.com/en/2.3.x/) are pretty tough to navigate, but they may become easier to handle once you go through tutorials such as [this particular Flask-SQLAlchemy tutorial playlist](https://www.youtube.com/playlist?list=PLXmMXHVSvS-BlLA5beNJojJLlpE0PJgCW). ORMs are pretty unintuitive, so I strongly recommend finding people that do understand and have them break it down for you.
- [This answer here](https://stackoverflow.com/a/51310699) informed me that I need to access the SQL query *statement* itself in order for Pandas' `read_sql()` function to work.

## FINAL NOTES
> Project completed on June 29, 2023
