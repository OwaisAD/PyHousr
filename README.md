# PyHousr

## Table of content

- [Python_eksamen](#Python_eksamen)
  - [Table of content](#table-of-content)
  - [About](#about)
  - [Setup project instructions](#Setup-project-instructions)
  - [Extend project](#Extend-project)
  - [Status](#status)
  - [List of Challenges](#List-of-Challenges)
  - [Other documents](#Other-documents)

## About

Semester project, 4th semester, Python Data Science application using Python, Selenium, Geopy, Pandas, Numpy, Tkinter, Matplotlib, Sklearn.
<br>

## Setup project instructions

1. Install the following packages:
   - selenium
   - pandas
   - numpy
   - customtkinter and tk
   - maplotlib
   - sklearn
   - geopy

Run the following command in the terminal to invoke the GUI

```
python3 UI.py
```

or you might need to use

```
python UI.py
```

If you'd like extend the project with additional cities, then check out the following section.
<br>

## Extend project

If you want to scrape data for additional cities, it is a 2 step process:
First you have to scrape the house links from dingeo.dk. This can be achieved by running the file "link_scraper.py" with the city zipcode as the argument, for example:

```
python3 link_scraper.py 4000
```

This will create a file in the ./data/link_data directory.

Secondly you have to scrape the house data. This can be achieved with the following command using zip_code 4000 as an argument:

```
python3 house_data_scraper.py 4000
```

You may have to create a file in ./data/house_data called:
house_data_4000.csv
and add the following headers: <br>

```
Address,X,Y,Price,Type,Size,Squaremeter price,Energy class,Url
```

If you want the models and UI to include your newly scraped house_data, you have to add the zip code of the city to the lists in each model and UI under the following files:

- ./notebooks/LinearRegression.ipynb
- ./notebooks/RandomTreeRegression.ipynb
- ./GUI/UI.py

## Status

What has been done (and if anything: what hasn't been done)
vi lykkedes med det vi havde sat op fra start - vi kom i mål

## List of Challenges

The things in project you want to highlight

## Other documents

Brainstorming can be found [here](https://docs.google.com/document/d/1BFdvE4-UCWUdEFiJL24s-s-r8a0LO03WU1U8LXW24tU/edit)
