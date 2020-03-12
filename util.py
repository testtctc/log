#coding=utf-8

def unique_values(d:dict):
    """字典中值的唯一值"""
    return list(set( value for value in d.values()))