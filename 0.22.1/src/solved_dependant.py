from di import Container, Dependant
from di.types.solved import SolvedDependency


# Framework code
class Request:
    ...


def web_framework():
    container = Container()
    solved = container.solve(Dependant(controller))
    assert isinstance(solved, SolvedDependency)

    container.execute_sync(solved, values={Request: Request()})

    container.execute_sync(solved, validate_scopes=False, values={Request: Request()})

    dependencies = solved.get_flat_subdependants()
    assert all(isinstance(item, Dependant) for item in dependencies)
    assert set(dependant.call for dependant in dependencies) == {Request, MyClass}


# User code
class MyClass:
    ...


def controller(request: Request, myobj: MyClass) -> None:
    ...
