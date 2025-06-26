import { Button, Popover } from 'antd';
import * as echarts from 'echarts';
import React, { useEffect, useRef } from 'react';
import { SketchPicker } from 'react-color';

const EchartsRenderer = ({ option, height = 300 }) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const instanceRef = useRef<echarts.EChartsType>();
  const [color, setColor] = React.useState('#5470c6');

  useEffect(() => {
    if (!chartRef.current) return;

    if (!instanceRef.current) {
      instanceRef.current = echarts.init(chartRef.current);
    }

    const newOption = {
      ...option,
      color: option.color || [color],
    };

    instanceRef.current.setOption(newOption, true);
  }, [option, color]);

  return (
    <div>
      <Popover
        content={
          <SketchPicker
            color={color}
            onChangeComplete={(col) => setColor(col.hex)}
          />
        }
        title="自定义配色"
        trigger="click"
      >
        <Button size="small" style={{ marginBottom: 8 }}>
          🎨 配色
        </Button>
      </Popover>
      <div ref={chartRef} style={{ width: '100%', height }}></div>
    </div>
  );
};

export default EchartsRenderer;
