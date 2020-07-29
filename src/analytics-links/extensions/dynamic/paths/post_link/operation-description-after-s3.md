CAUTION: When creating a link to the Amazon S3 service, be sure to follow best practices for security.
AWS root account credentials should never be used.
The policy for the created IAM User roles should be as strict as possible and only allow access to the required data and required resources.
You only need to know the Access Key Id and the Secret Access Key for the created IAM User role to access the S3 service.
The link will be able to access whatever is assigned to the IAM User, since it will be using the IAM User credentials to interact with the AWS S3 service.
