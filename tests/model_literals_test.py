from tests.utils import n4_parse, nt_parse

### Strings

def test_string_double_quoted():
  n4_graph = n4_parse('examples/model_literals/strings-double_quoted.n4')
  expected_graph = nt_parse('examples/model_literals/strings.nt')
  assert n4_graph == expected_graph 

def test_string_single_quoted():
  n4_graph = n4_parse('examples/model_literals/strings-single_quoted.n4')
  expected_graph = nt_parse('examples/model_literals/strings.nt')
  assert n4_graph == expected_graph 

def test_string_double_multiline():
  n4_graph = n4_parse('examples/model_literals/strings-multiline_double.n4')
  expected_graph = nt_parse('examples/model_literals/strings.nt')
  assert n4_graph == expected_graph 

def test_string_single_multiline():
  n4_graph = n4_parse('examples/model_literals/strings-multiline_single.n4')
  expected_graph = nt_parse('examples/model_literals/strings.nt')
  assert n4_graph == expected_graph 


### Integers

def test_integers():
  n4_graph = n4_parse('examples/model_literals/integers.n4')
  expected_graph = nt_parse('examples/model_literals/integers.nt')
  assert n4_graph == expected_graph


### Decimals

def test_decimals():
  n4_graph = n4_parse('examples/model_literals/decimals.n4')
  expected_graph = nt_parse('examples/model_literals/decimals.nt')
  assert n4_graph == expected_graph


### Rationals

def test_rationals():
  n4_graph = n4_parse('examples/model_literals/rationals.n4')
  expected_graph = nt_parse('examples/model_literals/rationals.nt')
  assert n4_graph == expected_graph
  

### Booleans

def test_booleans():
  n4_graph = n4_parse('examples/model_literals/boolean.n4')
  expected_graph = nt_parse('examples/model_literals/boolean.nt')
  assert n4_graph == expected_graph


### Dates and times

#### Dates

def test_dates_simple():
  n4_graph = n4_parse('examples/model_literals/dates_simple.n4')
  expected_graph = nt_parse('examples/model_literals/dates_simple.nt')
  assert n4_graph == expected_graph

def test_dates_with_tz():
  n4_graph = n4_parse('examples/model_literals/dates_with_tz.n4')
  expected_graph = nt_parse('examples/model_literals/dates_with_tz.nt')
  assert n4_graph == expected_graph

#### Times

def test_times_simple():
  n4_graph = n4_parse('examples/model_literals/times_simple.n4')
  expected_graph = nt_parse('examples/model_literals/times_simple.nt')
  assert n4_graph == expected_graph

def test_times_with_tz():
  n4_graph = n4_parse('examples/model_literals/times_with_tz.n4')
  expected_graph = nt_parse('examples/model_literals/times_with_tz.nt')
  assert n4_graph == expected_graph

def test_times_with_fractional_secs():
  n4_graph = n4_parse('examples/model_literals/times_with_fractional_secs.n4')
  expected_graph = nt_parse('examples/model_literals/times_with_fractional_secs.nt')
  assert n4_graph == expected_graph

def test_times_with_tz_and_fractional_secs():
  n4_graph = n4_parse('examples/model_literals/times_with_tz_and_fractional_secs.n4')
  expected_graph = nt_parse('examples/model_literals/times_with_tz_and_fractional_secs.nt')
  assert n4_graph == expected_graph

#### Datetimes

def test_datetimes_simple():
  n4_graph = n4_parse('examples/model_literals/datetimes_simple.n4')
  expected_graph = nt_parse('examples/model_literals/datetimes_simple.nt')
  assert n4_graph == expected_graph

def test_datetimes_with_tz():
  n4_graph = n4_parse('examples/model_literals/datetimes_with_tz.n4')
  expected_graph = nt_parse('examples/model_literals/datetimes_with_tz.nt')
  assert n4_graph == expected_graph

def test_datetimes_with_fractional_secs():
  n4_graph = n4_parse('examples/model_literals/datetimes_with_fractional_secs.n4')
  expected_graph = nt_parse('examples/model_literals/datetimes_with_fractional_secs.nt')
  assert n4_graph == expected_graph

def test_datetimes_with_tz_and_fractional_secs():
  n4_graph = n4_parse('examples/model_literals/datetimes_with_tz_and_fractional_secs.n4')
  expected_graph = nt_parse('examples/model_literals/datetimes_with_tz_and_fractional_secs.nt')
  assert n4_graph == expected_graph

#### Durations

def test_durations():
  n4_graph = n4_parse('examples/model_literals/durations.n4')
  expected_graph = nt_parse('examples/model_literals/durations.nt')
  assert n4_graph == expected_graph

### Language strings

def test_simple_language():
  n4_graph = n4_parse('examples/model_literals/langstring_simple.n4')
  expected_graph = nt_parse('examples/model_literals/langstring_simple.nt')
  assert n4_graph == expected_graph

def test_language_with_dialect():
  n4_graph = n4_parse('examples/model_literals/langstring_dialect.n4')
  expected_graph = nt_parse('examples/model_literals/langstring_dialect.nt')
  assert n4_graph == expected_graph

### Other datatypes

def test_custom_data_types():
  n4_graph = n4_parse('examples/model_literals/custom_datatypes.n4')
  expected_graph = nt_parse('examples/model_literals/custom_datatypes.nt')
  assert n4_graph == expected_graph