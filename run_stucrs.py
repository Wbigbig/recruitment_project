#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author   :

# 作为 stucrs 项目的运行主模块

from stucrs import create_app

app = create_app()

if __name__ == '__main__':
	
	app.run(debug=True, host='0.0.0.0')