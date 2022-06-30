import psycopg2 as sq


def IsRegistration(fromId):
    global base, cur
    base = sq.connect(dbname='d9882ng2h7srs6', user='rixdvqeatezwpn',
                      password='60e4ac9ad7bcb8be1b8900f38fc0c70a52a69fb6dcdd59bf553c6262631f54a6', host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
    cur=base.cursor()
    cur.execute(f"SELECT COUNT(*) FROM profile WHERE id='{fromId}'")
    result=cur.fetchall()
    if result[0] == (1,):
        return True
    return False