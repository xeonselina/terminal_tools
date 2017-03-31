import gevent
from gevent.pool import Group


group = Group()


def talk(msg):
    if msg == 'foo':
        print 'foo1'
        group.add(g3)
        print 'foo1 add g3'
        print ''
    while 1:
        gevent.sleep(2)
        print(msg)

g1 = gevent.spawn(talk, 'bar')
g2 = gevent.spawn(talk, 'foo')
g3 = gevent.spawn(talk, 'fizz')
group.add(g1)
group.add(g2)
group.join()



