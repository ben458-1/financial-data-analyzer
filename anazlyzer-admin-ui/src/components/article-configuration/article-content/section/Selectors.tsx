import React, { useState } from 'react';
import { Button, Space } from 'antd';
import Selector from './Selector';
import { Selector as SelectorProps } from '../ArticleContentConfiguration';

interface SelectorsProps {
    selectors?: SelectorProps[];
    sectionName: string;
    onSelectorsChange?: (selectors: SelectorProps[]) => void;
}

const Selectors: React.FC<SelectorsProps> = ({ selectors: SelectorProps, onSelectorsChange }) => {
    const [selectors, setSelectors] = useState<SelectorProps[]>(SelectorProps || []);

    const updateSelectors = (updated: SelectorProps[]) => {
        setSelectors(updated);
        onSelectorsChange?.(updated);
    };

    const handleChange = (index: number, updated: SelectorProps) => {
        const newSelectors = [...selectors];
        newSelectors[index] = updated;
        updateSelectors(newSelectors);
    };

    const handleDelete = (index: number) => {
        updateSelectors(selectors.filter((_, i) => i !== index));
    };

    const handleAdd = () => {
        updateSelectors([...selectors, { name: '', type: 'css', regex: [] }]);
    };

    return (
        <div>
            <Space size={[3, 6]} align="center" wrap>
                {selectors.map((selector, index) => (
                    <Selector
                        key={index}
                        selector={selector}
                        onChange={(updated) => handleChange(index, updated)}
                        onDelete={() => handleDelete(index)}
                    />
                ))}
            </Space>
            <div style={{ marginTop: 10 }}><Button type="dashed" onClick={handleAdd} block disabled={selectors.some(sel => !sel.name || !sel.type)}>Add Selector</Button></div>
        </div>
    );
};


export default Selectors;
