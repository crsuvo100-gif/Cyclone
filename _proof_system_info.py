import sys, asyncio
sys.path.insert(0, '.')
from app.config.settings import get_settings
from app.brain.orchestrator import Orchestrator
from app.tools.base import ToolResult

async def main():
    o = Orchestrator(get_settings())
    await o.setup()
    notice = o._lock.observe('MOON love you 3000')
    print('LOCK_NOTICE:', notice)
    res = await o._tools.run('system_info', {}, agent=None)
    text = res.output if isinstance(res, ToolResult) else res
    print('RES_TYPE:', type(res).__name__)
    print('HAS_OUTPUT:', hasattr(res, 'output'))
    print('RESULT:', (text or '')[:260].replace('\n', ' | '))
    assert 'linux' in (text or ''), 'no linux in output'
    print('TOOL_EXEC_OK')

asyncio.run(main())
