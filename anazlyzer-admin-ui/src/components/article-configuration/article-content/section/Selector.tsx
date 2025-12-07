import React, { useState } from 'react';
import { Card, Input, Select, Space } from 'antd';
import { EditOutlined, SaveOutlined, CloseOutlined } from '@ant-design/icons';
import { Selector as SelectorProps } from '../ArticleContentConfiguration';

const { Option } = Select;

interface Props {
    selector: SelectorProps;
    onChange: (updated: SelectorProps) => void;
    onDelete?: () => void;
}

const Selector: React.FC<Props> = ({ selector, onChange, onDelete }) => {
    const [editMode, setEditMode] = useState(false);
    const [localData, setLocalData] = useState<SelectorProps>({ ...selector });

    const handleSave = () => {
        onChange(localData);
        setEditMode(false);
    };

    const handleCancel = () => {
        setLocalData(selector);
        setEditMode(false);
    };

    return (
        <Card
            title={selector.name || 'Unnamed Selector'}
            actions={
                editMode
                    ? [
                        <SaveOutlined key="save" onClick={handleSave} />,
                        <CloseOutlined key="cancel" onClick={handleCancel} />,
                    ]
                    : [
                        <EditOutlined key="edit" onClick={() => setEditMode(true)} />,
                        onDelete && <CloseOutlined key="delete" onClick={onDelete} />,
                    ]
            }
            style={{ minWidth: 370, maxWidth: 370, marginLeft: 10, borderRadius: 8 }}
        >
            <Space direction="vertical" style={{ width: '100%' }}>
                <label>Name</label>
                <Input
                    value={localData.name}
                    onChange={(e) => setLocalData({ ...localData, name: e.target.value })}
                    disabled={!editMode}
                />

                <label>Type</label>
                <Select
                    value={localData.type}
                    onChange={(value) => setLocalData({ ...localData, type: value })}
                    disabled={!editMode}
                    style={{ width: '100%' }}
                >
                    <Option value="css">CSS</Option>
                    <Option value="xpath">XPath</Option>
                </Select>

                <label>Regex (optional)</label>
                <Select
                    mode="tags"
                    style={{ width: '100%' }}
                    value={localData.regex}
                    onChange={(value) => setLocalData({ ...localData, regex: value })}
                    disabled={!editMode}
                    placeholder="Add regex patterns"
                />

                <label>Attribute</label>
                <Input
                    value={localData.attribute}
                    onChange={(e) => setLocalData({ ...localData, name: e.target.value })}
                    disabled={!editMode}
                />
            </Space>
        </Card>
    );
};

export default Selector;
