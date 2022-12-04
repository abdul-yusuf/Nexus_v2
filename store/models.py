from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=50)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)
    description = models.CharField(max_length=150)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    sub_category = models.ForeignKey('Sub_Category', on_delete=models.CASCADE, blank=True, null=True)

    @property
    def rate(self):
        l=[]
        rt = self.ratings

        for x in [rt.rate1,rt.rate2,rt.rate3,rt.rate4,rt.rate5]:
            # if x==1:
            l.append(x)
            # else:
                # print('else')
                # self.calc()
                # pass
        if l==[1,1,1,1,1]:
            # print('yes')
            return 0
        else:
            # print('else')
            return self.calc()
        # print(l)
    def calc(self): 
        # print(dir(self.ratings))  
        # print('we in') 
        ratex = self.ratings
        summ = ratex.rate1+ratex.rate2*2+ratex.rate3*3+ratex.rate4*4+ratex.rate5*5
        sumz = ratex.rate1+ratex.rate2+ratex.rate3+ratex.rate4+ratex.rate5
        rates = summ/sumz
        return round(rates,1)
    
    @property
    def discount_percent(self):
        try:
            per = (int(self.discount_price)/int(self.price))*100
            return round(per,0)
        except TypeError:
            return 0

    def __str__(self) -> str:
        return self.title

class Vendor(models.Model):
    owner = models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name='vendor')
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Rating(models.Model):
    """
    Rating System on a Scale of (5)
    """
    product = models.OneToOneField('Product', on_delete=models.CASCADE, blank=True, null=True, related_name='ratings')
    rate1 = models.IntegerField(default=1)
    rate2 = models.IntegerField(default=1)
    rate3 = models.IntegerField(default=1)
    rate4 = models.IntegerField(default=1)
    rate5 = models.IntegerField(default=1)
    
class Category(models.Model):
    title = models.CharField(max_length=25)

class Sub_Category(models.Model):
    title = models.CharField(max_length=25)
    parent_category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)

class Images(models.Model):
    product = models.OneToOneField('Product', on_delete=models.CASCADE, blank=True, null=True, related_name='images')
    image1 = models.ImageField()
    image2 = models.ImageField(blank=True, null=True)
    image3 = models.ImageField(blank=True, null=True)
    image4 = models.ImageField(blank=True, null=True)
    image5 = models.ImageField(blank=True, null=True)


class Coupon(models.Model):
    code = models.CharField(max_length=11)
    amount = models.FloatField()

    def __str__(self) -> str:
        return self.code

class Review(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True, related_name='reviews')
    massage = models.CharField(max_length=150)
    reply = models.ForeignKey('ReviewReply', on_delete=models.CASCADE, blank=True, null=True)
    stars = models.IntegerField()

    def save(self, *args, **kwargs) -> None:
        instance = self.product.ratings
        if self.stars==1:
            instance.rate1+=1
            instance.save()
        elif self.stars==2:
            instance.rate2+=1
            instance.save()
        elif self.stars==3:
            instance.rate3+=1
            instance.save()
        elif self.stars==4:
            instance.rate4+=1
            instance.save()
        elif self.stars==5:
            instance.rate5+=1
            instance.save()
        return super().save(*args, **kwargs)
    # def rating(self):
        
class ReviewReply(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, blank=True, null=True)
    massage = models.TextField()
