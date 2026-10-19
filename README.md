# ShelfShare

A small local lend-board. Open the page, see a few fictional Hong Kong listings, and request one item. The status changes from `available` to `requested`. There are no accounts.

Author: Zhenhua Liu.

Listings use neighbourhood names only. They are sample data, not real offers, and this app is not connected to any community or school.

## Run

Requires Python 3. No extra packages.

```bash
cd /workspace/shelfshare
python3 app.py
```

Then open http://127.0.0.1:8787

The server listens only on `127.0.0.1`, port **8787**. Stop it with Ctrl+C.

Requesting an item sends `POST /api/listings/<id>/request` and writes the new status to `data/listings.json`. `GET /api/listings` returns the board.

To put every item back to `available`, edit `data/listings.json` and set each `status` to `available`, then reload the page.

## 中文

这是一个只在本机运行的借用板。页面上有几件虚构的香港物品，只写地区，不写人名。点 Request 之后，状态会从 available 变成 requested。不需要注册账号。启动命令是 `python3 app.py`，地址是 http://127.0.0.1:8787 。
