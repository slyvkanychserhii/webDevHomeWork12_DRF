# webDevHomeWork12_DRF

---

Для установки mysqlclient на MacOS:

https://pypi.org/project/mysqlclient/

mac os global environment run: ->

```
brew install mysql-client pkg-config
```

in your virtualenv or other environment ->

```
export PKG_CONFIG_PATH="$(brew --prefix)/opt/mysql-client/lib/pkgconfig"
```

```
pip install -r requirements.txt
```
