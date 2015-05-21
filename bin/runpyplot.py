#!/usr/bin/env python2.7

try:
  activate_this = './bin/activate_this.py'
  execfile(activate_this, dict(__file__=activate_this))
except:
  pass


import click
from pyplot import *


@click.command()
@click.option("-c", help="pyplot command")
@click.option("-prefix", help="R commands to prefix")
@click.option("-csv", type=str, help="CSV file to load into var \"data\"")
@click.option("-db", help="Database name if using -sql")
@click.option("-sql", help="SQL query to use as dataset.  Loaded in var \"data\"")
@click.option("-o", help="Output file to save graphic.  Else print program and exit")
@click.option("-w", type=float, default=10, help="width of output file")
@click.option("-h", type=float, default=8, help="height of output file")
@click.option("-scale", type=float, default=1.0, help="scaling of output file")
def main(c, prefix, csv, db, sql, o, w, h, scale):
  """
  ggplot2 syntax in Python.

  Run pyplot command from command line

    python pyplot -c "ggplot('diamonds', aes('carat', 'price')) + geom_point()"

  Import into your python program to use ggplot

    \b
    from pyplot import *
    p = ggplot('diamonds', aes('carat', y='price')) + geom_point()
    p = p + facet_wrap(None, "color")

    \b
    # set prefix so that 'diamonds' is loaded in R
    prefix = \"\"\" ...R code to load data into diamonds variable...  \"\"\"
    p.save("test.pdf", prefix=prefix)


  Use convenience functions for loading data from postgres or a CSV

    \b
    # load from database query
    prefix = data_sql('DBNAME', 'SELECT * FROM T')

    \b
    # load from CSV file.  Takse same arguments as R's read.csv
    prefix = data_csv("FILENAME", sep=',')


  Caveats: Does not copy and import data between python and R, so pyplot depends on setting the prefix to load the appropriate data into an R variable so that ggplot can load it:
  """

  if not c: 
    print "no command.  exiting"
    return

  prefix = filter(bool, [prefix])

  if csv:
    csvprefix = data_csv(csv)
    if csvprefix:
      prefix.append(csvprefix)
  else:
    sqlprefix = data_sql(db, sql)
    if sqlprefix:
      prefix.append(sqlprefix)
  prefix = "\n".join(prefix)

  c = "plot = %s" % c
  exec c
  plot.save(o, prefix=prefix, width=w, height=h, scale=scale)


if __name__ == "__main__":
  main()