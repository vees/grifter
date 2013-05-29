from regatta.models import Moment
m=Moment.objects.filter(pk=1)[0]
print str(m.best_guess())

