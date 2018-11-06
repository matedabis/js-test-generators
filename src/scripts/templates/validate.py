#!/usr/bin/env python

validate = '''
function validate(test_value, expected_value, false_values) {
    var radix = 2 + Math.abs(expected_value % 35);
    assert(test_value === expected_value);
    assert(test_value.toString(radix) === expected_value.toString(radix));
    for (var i in false_values) {
        radix = 2 + Math.abs(false_values[i] % 35);
        assert(test_value !== false_values[i]);
        assert(test_value.toString(radix) !== false_values[i].toString(radix));
    }
}
'''
