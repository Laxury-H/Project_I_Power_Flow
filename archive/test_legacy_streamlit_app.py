from pathlib import Path
from streamlit.testing.v1 import AppTest


def test_streamlit_example_runs():
    """Examples, reruns, changed inputs and failure must not leak stale results."""
    app = Path(__file__).resolve().parents[1] / 'app.py'
    at = AppTest.from_file(str(app)).run(timeout=20)
    assert not at.exception
    at.button[0].click().run(timeout=20)
    assert not at.exception
    assert 'Converged' in at.success[0].value
    assert at.metric[0].value == '2.204693'
    at.run()
    assert 'Converged' in at.success[0].value
    assert len(at.get('download_button')) == 3
    at.slider[0].set_value(120).run()
    assert not at.success and not at.metric
    at.button[0].click().run()
    assert at.metric[0].value == '2.834110'
    at.selectbox[0].select('5bus').run()
    assert not at.success
    at.slider[0].set_value(100).run()
    at.button[0].click().run()
    assert not at.exception
    assert 'Converged' in at.success[0].value
    assert at.metric[0].value == '3.650487'
    at.number_input[1].set_value(0).run()
    assert not at.success and not at.metric
    at.button[0].click().run()
    assert 'Maximum iterations' in at.error[0].value
    assert not at.success and len(at.get('download_button')) == 0
