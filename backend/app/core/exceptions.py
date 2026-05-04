class ProjectHelperError(Exception):
    pass


class GitCloneError(ProjectHelperError):
    pass


class PathTraversalError(ProjectHelperError):
    pass


class ProjectNotFoundError(ProjectHelperError):
    pass


class AnalysisError(ProjectHelperError):
    pass
