"""Simple integration tests for the AWS S3 actors."""

from nose.plugins.attrib import attr
import logging

from tornado import testing

# from kingpin import utils
# from kingpin.actors import exceptions
from kingpin.actors.aws import s3

__author__ = 'Matt Wise <matt@nextdoor.com>'

log = logging.getLogger(__name__)
logging.getLogger('boto').setLevel(logging.INFO)


class IntegrationS3(testing.AsyncTestCase):

    """High level S3 Actor testing.

    These tests will check two things:
    * Creation of S3 buckets with a variety of options
    * Updating these S3 buckets with new parameters
    * Destroying the S3 buckets

    Requirements:
        You have to create an S3 Bucket named kingpin-integration-test and
        place it in the specified region (default us-east-1).
        As with other tests, environment variables AWS_ACCESS_KEY_ID and
        AWS_SECRET_ACCESS_KEY are expected, and the key should have
        permissions to read S3 bucket information.

    Note, these tests must be run in-order. The order is defined by
    their definition order in this file. Nose follows this order according
    to its documentation:

        http://nose.readthedocs.org/en/latest/writing_tests.html
    """

    integration = True

    bucket_name = 'kingpin-integration-test'
    region = 'us-east-1'

    @attr('aws', 'integration')
    @testing.gen_test(timeout=60)
    def integration_01a_create_bucket(self):
        actor = s3.Bucket(
            options={
                'name': self.bucket_name,
                'region': self.region,
                'state': 'present',
            }
        )
        done = yield actor.execute()
        self.assertEquals(done, None)

    @attr('aws', 'integration')
    @testing.gen_test(timeout=60)
    def integration_01b_set_bucket_policy(self):
        actor = s3.Bucket(
            options={
                'name': self.bucket_name,
                'region': self.region,
                'state': 'present',
                'policy': 'examples/aws.s3/amazon_put.json',
            }
        )
        done = yield actor.execute()
        self.assertEquals(done, None)

    @attr('aws', 'integration')
    @testing.gen_test(timeout=60)
    def integration_01c_delete_bucket_policy(self):
        actor = s3.Bucket(
            options={
                'name': self.bucket_name,
                'region': self.region,
                'state': 'present',
                'policy': '',
            }
        )
        done = yield actor.execute()
        self.assertEquals(done, None)

    @attr('aws', 'integration')
    @testing.gen_test(timeout=60)
    def integration_09_delete_bucket(self):
        actor = s3.Bucket(
            options={
                'name': self.bucket_name,
                'region': self.region,
                'state': 'absent',
            }
        )
        done = yield actor.execute()
        self.assertEquals(done, None)