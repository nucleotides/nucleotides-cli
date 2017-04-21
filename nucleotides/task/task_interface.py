import abc

def select_task(c):
    from nucleotides.task.short_read_assembler           import ShortReadAssemblerTask
    from nucleotides.task.reference_assembly_evaluation  import ReferenceAssemblyEvaluationTask
    return {
            'short_read_assembler'          : ShortReadAssemblerTask,
            'reference_assembly_evaluation' : ReferenceAssemblyEvaluationTask
            }[c]



class TaskInterface(object):
    __metaclass__ = abc.ABCMeta

    def before_container_hook(self, app):
        """
        Hook into process of creating a Docker container before launch. Can be used
        to perform any specific actions required before launching
        """
        return


    def was_successful(self, app, output_files):
        """
        Given the current state of the nucleotides directory, and a list of output
        files determines if the benchmarking task was successful. Return a tuple
        containing a boolean and a dictionary of benchmarking metrics.
        """
        created_files = map(lambda x: x['type'], output_files)
        is_successful = self.successful_event_output_files().issubset(created_files)
        metrics = self.collect_metrics(app) if is_successful else {}
        return (is_successful, metrics)


    @abc.abstractmethod
    def biobox_args(self, app):
        """
        Create the biobox dictionary used to populate the biobox.yaml file given
        to the biobox Docker image.
        """
        return


    @abc.abstractmethod
    def output_file_paths(self, app):
        """
        List the paths of the generated biobox files. These are the files that
        should be collected and uploaded to nucleotides after the task has been
        completed.
        """
        return


    @abc.abstractmethod
    def collect_metrics(self, app):
        """
        After the biobox docker image has completed, return a dictionary of all
        metrics generated by running the container.
        """
        return


    @abc.abstractmethod
    def successful_event_output_files(self):
        """
        List the files that should be produced upon successful completion of the
        biobox container execution
        """
        return
