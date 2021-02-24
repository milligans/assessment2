import datetime

class TheNow(): 
  def __init__(self):
    self.blog_year=datetime.datetime.now().year
    self.blog_date=datetime.datetime.now().day
    self.blog_month=datetime.datetime.now().month
   
  def sentence(self):
    return f"Today's date is {self.blog_date}/{self.blog_month}/{self.blog_year}"