import React, { useEffect, useState } from "react";
import { Doc } from "../ArticleMetadataConfiguration";
import { Button, Collapse, Form, Input, Select, Space } from "antd";
import { Selector as SelectorProp } from '../../article-content/ArticleContentConfiguration';
import Selectors from "../../article-content/section/Selectors";
import Selector from "../../article-content/section/Selector";



const { Panel } = Collapse;
const { Option } = Select;


export const DateForm: React.FC<{ doc: Doc; onUpdate: (field: string, value: string | boolean | number) => void; }> = ({ doc, onUpdate }) => {
    const [editMode, setEditMode] = useState(false);
    const [form] = Form.useForm();

    useEffect(() => {
        form.setFieldsValue(doc);
    }, [doc]);

    const handleSave = async () => {
        try {
            const values = await form.validateFields();
            Object.entries(values).forEach(([key, value]) => {
                onUpdate(key, value);
            });
            setEditMode(false);
        } catch (error) {
            console.error('Validation Failed:', error);
        }
    };

    const handleCancel = () => {
        form.setFieldsValue(doc);
        setEditMode(false);
    };

    return (
        <>
            <Form form={form} layout="vertical" initialValues={doc}>
                <Form.Item label="Date Regex" name="dateRegex">
                    <Input
                        placeholder="Enter date regex"
                        readOnly={!editMode}
                        style={{
                            backgroundColor: !editMode ? '#f5f5f5' : undefined,
                            cursor: !editMode ? 'not-allowed' : 'auto',
                        }}
                    />
                </Form.Item>

                <Form.Item label="Time Regex" name="timeRegex">
                    <Input
                        placeholder="Enter time regex"
                        readOnly={!editMode}
                        style={{
                            backgroundColor: !editMode ? '#f5f5f5' : undefined,
                            cursor: !editMode ? 'not-allowed' : 'auto',
                        }}
                    />
                </Form.Item>

                <Form.Item label="Date Regex Desc" name="dateRegexDesc">
                    <Input
                        placeholder="Enter date regex desc"
                        readOnly={!editMode}
                        style={{
                            backgroundColor: !editMode ? '#f5f5f5' : undefined,
                            cursor: !editMode ? 'not-allowed' : 'auto',
                        }}
                    />
                </Form.Item>

                <Form.Item label="Time Regex Desc" name="timeRegexDesc">
                    <Input
                        placeholder="Enter time regex desc"
                        readOnly={!editMode}
                        style={{
                            backgroundColor: !editMode ? '#f5f5f5' : undefined,
                            cursor: !editMode ? 'not-allowed' : 'auto',
                        }}
                    />
                </Form.Item>

                {editMode ? (
                    <Form.Item>
                        <Space>
                            <Button type="primary" onClick={handleSave}>
                                Save
                            </Button>
                            <Button onClick={handleCancel}>Cancel</Button>
                        </Space>
                    </Form.Item>
                ) : (
                    <Form.Item>
                        <Button onClick={() => setEditMode(true)}>Edit</Button>
                    </Form.Item>
                )}
            </Form>
        </>
    );
};

const DefaultSelectors: React.FC<Doc> = (config) => {

    const updateField = (field: keyof Doc, value: string | boolean | number) => {
        console.log(`Field "${field}" updated to:`, value);
        // TODO: Implement state update or API PATCH logic
    };



    const handleChange = (updated: SelectorProp) => {
        console.log(updated);
    };

    const handleSave = () => {
        setEditMode(false);
        console.log("Saving:", value);
    };

    const [editMode, setEditMode] = useState(false);


    const sections = [
        { key: '1', header: 'Headline', content: <Selectors selectors={config.headline} sectionName='Headline Selectors'></Selectors> },
        { key: '2', header: 'Metadata', content: <Selectors selectors={config.metadata} sectionName='Metadata Selectors'></Selectors> },
        { key: '3', header: 'News URL', content: <Selectors selectors={config.newsUrl} sectionName='News URL Selectors'></Selectors> },
        {
            key: '4', header: 'Date', content: <>
                <div>
                    <DateForm doc={config} onUpdate={updateField}></DateForm>
                </div>
                <div><Selectors selectors={config.date} sectionName='Date Selectors'></Selectors></div>
            </>
        },
        { key: '5', header: 'Preamble', content: <Selectors selectors={config.preamble} sectionName='Preamble Selector'></Selectors> },
        { key: '6', header: 'Loop Section', content: <Selectors selectors={config.loopSection} sectionName='Loop Section Selector'></Selectors> },
        { key: '7', header: 'Search Sector Type', content: <Selectors selectors={config.searcSectorType} sectionName='Search Sector Type Selector'></Selectors> },
        {
            key: '8', header: 'next', content: <>
                <Space direction="vertical" style={{ width: '100%' }}>
                    <label>Method</label>
                    <Select
                        value={config.next.method}
                        style={{ width: '50%', marginBottom: '20px' }}
                    >
                        <Option value="click">Click</Option>
                    </Select>
                </Space>
                <div>
                    <Selector
                        selector={config.next.element}
                        onChange={(updated) => handleChange(updated)}
                    />
                </div>
            </>
        },
        {
            key: '9', header: 'popup', content: <>
                <Space direction="vertical" style={{ width: '100%' }}>
                    <label>Method</label>
                    <Select
                        value={config.popup.method}
                        style={{ width: '50%', marginBottom: '20px' }}
                    >
                        <Option value="click">Click</Option>
                    </Select>
                </Space>
                <div>
                    <Selector
                        selector={config.popup.element}
                        onChange={(updated) => handleChange(updated)}
                    />
                </div>
            </>
        },
    ];

    return (
        <>
            <Collapse style={{ paddingTop: '8px', borderRadius: '8px' }}>
                {sections.map(item => (
                    <Panel
                        header={<span style={{ fontWeight: 'bold' }}>{item.header}</span>}
                        key={item.key}
                        showArrow={false}
                        style={{ marginBottom: '8px', borderRadius: '8px', }}
                    >
                        <div>{item.content}</div>
                    </Panel>
                ))}
            </Collapse>
        </>
    );
}


export default DefaultSelectors;