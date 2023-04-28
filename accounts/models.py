from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser


class AccountManager(BaseUserManager):
    def create_user(self, username, email, password=None, is_reseller=False, reseller=1):
        """Creates and saves a User with the given email, username, password and extra fields"""
        if not email:
            raise ValueError("User must have an valid email")
        if not username:
            raise ValueError("User must have an username")
        if reseller:
            reseller = Account.objects.get(id=reseller)
            print(reseller)

        user = self.model(
                email = self.normalize_email(email),
                username = username,
                is_reseller = is_reseller,
                reseller = reseller,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, reseller=None):
        """Creates and saves a Superuser with the given email, username, password and extra fields"""
        user = self.create_user(username, email, password, reseller=reseller)

        user.is_staff = True
        user.is_superuser = True
        user.is_reseller = True
        user.reseller = None
        user.save(using=self._db)
        return user
    

class Account(AbstractBaseUser):
    # Auth Details
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=20)

    # Profile Details
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)

    # Company Details
    company_name = models.CharField(max_length=50)
    gst_number = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    # Required Fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    # Permissions Fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_reseller = models.BooleanField(default=False)

    # App Permissions
    whtsapp_app = models.BooleanField(default=True)
    voice_app = models.BooleanField(default=False)

    # Reseller End User Mapper
    reseller = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='belongs_to')

    # Wallet Balance
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_staff
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True