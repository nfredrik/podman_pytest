import pytest

def test_print_hi(log, myarg):
    # Use a breakpoint in the code line below to debug your script.
    log, more = log
    log.info(f'Hi, kalle')  # Press ⌘F8 to toggle the breakpoint.
    assert True

    log.warning(f'{myarg=}')

    log.warning(more)

    log.error('ERROR')

    log.critical('CRITICAL')
