from classes.account import Account
from classes.address import Address

class College(Account):
  def __init__(self, name: str, address: Address, phone, enrollment: int) -> None:
    super().__init__(name, address, phone)
    self.enrollment = enrollment

  def generate_sql(self):
    return f"""
      INSERT into colleges(name, address1, city, state, zip, phone, soundex, enrollment)
      VALUES(%s, %s, %s, %s ,%s, %s, %s, %s)
    """
  
  def execute_sql(self, cursor, sql):
    cursor.execute(sql, (self.name,
        self.address.address_1,
        self.address.city,
        self.address.state,
        self.address.zip,
        self.phone,
        self.soundex,
        self.enrollment)
    )
