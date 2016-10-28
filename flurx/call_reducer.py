from pyrsistent import PMap, PList
import inspect
import logging

logger = logging.getLogger(__name__)


def call_reducer(reducer, state, action):
    result = reducer(state, action)

    if not isinstance(result, (PMap, PList)):
        reducer_name = reducer.__name__
        source_file = inspect.getsourcefile(reducer)
        logger.warn("reduce function '%s' (defined in %s) didn't return persistent object on action %s" %
              (reducer_name, source_file, action))

    return result

