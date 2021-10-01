import oci
import pandas as pd

reporting_namespace = 'bling'
prefix_file = "reports/cost-csv"
file_location = '../OciConfig/config.prod'

config = oci.config.from_file(file_location=file_location, profile_name='NC')
object_storage_client = oci.object_storage.ObjectStorageClient(config)
reporting_bucket = config['tenancy']
report_bucket_objects = object_storage_client.list_objects(
                                                        reporting_namespace,
                                                        reporting_bucket,
                                                        prefix=prefix_file,
                                                        start_after=None,
                                                        end=None)
list_init = []
for o in report_bucket_objects.data.objects:
    list_init.append({'name': o.name, 'size': o.size, 'time_created': o.time_created})
df1 = pd.DataFrame(list_init)
print(df1.head())