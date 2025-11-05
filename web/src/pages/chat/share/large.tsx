import MessageInput from '@/components/message-input';
import MessageItem from '@/components/message-item';
import { useClickDrawer } from '@/components/pdf-drawer/hooks';
import { MessageType, SharedFrom } from '@/constants/chat';
import { useSendButtonDisabled } from '@/pages/chat/hooks';
import { Flex, Spin, Typography } from 'antd';
import React, { forwardRef, useMemo } from 'react';
import {
  useGetSharedChatSearchParams,
  useSendSharedMessage,
} from '../shared-hooks';
import { buildMessageItemReference } from '../utils';

import PdfDrawer from '@/components/pdf-drawer';
import { useFetchNextConversationSSE } from '@/hooks/chat-hooks';
import { useFetchFlowSSE } from '@/hooks/flow-hooks';
import i18n from '@/locales/config';
import { buildMessageUuidWithRole } from '@/utils/chat';
import { RightOutlined } from '@ant-design/icons';
import styles from './index.less';

const { Text } = Typography;

const ChatContainer = () => {
  const {
    sharedId: conversationId,
    data,
    from,
    locale,
    visibleAvatar,
  } = useGetSharedChatSearchParams();
  const { visible, hideModal, documentId, selectedChunk, clickDocumentButton } =
    useClickDrawer();

  const {
    handlePressEnter,
    handleInputChange,
    value,
    sendLoading,
    loading,
    ref,
    derivedMessages,
    hasError,
    stopOutputMessage,
    setValue, // 添加setValue以便更新输入框的值
  } = useSendSharedMessage();
  const sendDisabled = useSendButtonDisabled(value);

  // 定义可以问的问题列表
  const suggestedQuestions = [
    '请对我近期的健康状况进行全方位分析',
    '查询最近一次检验结果',
    '查询家庭医生签约信息',
    '查询慢病管理信息',
  ];

  // 点击建议问题时，将问题设置到输入框中
  const handleSuggestedQuestionClick = (question: string) => {
    setValue(question);
  };

  const useFetchAvatar = useMemo(() => {
    return from === SharedFrom.Agent
      ? useFetchFlowSSE
      : useFetchNextConversationSSE;
  }, [from]);
  React.useEffect(() => {
    if (locale && i18n.language !== locale) {
      i18n.changeLanguage(locale);
    }
  }, [locale, visibleAvatar]);
  const { data: avatarData } = useFetchAvatar();

  if (!conversationId) {
    return <div>empty</div>;
  }

  return (
    <>
      <Flex
        flex={1}
        className={styles.chatContainer}
        vertical
        style={{ background: '#F6F6F6' }}
      >
        <Flex flex={1} vertical className={styles.messageContainer}>
          <div>
            <Spin spinning={loading}>
              {derivedMessages?.map((message, i) => {
                return (
                  <div key={buildMessageUuidWithRole(message)}>
                    {i !== 0 &&
                      (!data || Object.hasOwn(data, 'showSuggestType')) && (
                        <MessageItem
                          visibleAvatar={visibleAvatar}
                          avatarDialog={avatarData?.avatar}
                          item={message}
                          nickname="You"
                          reference={buildMessageItemReference(
                            {
                              message: derivedMessages,
                              reference: [],
                            },
                            message,
                          )}
                          loading={
                            message.role === MessageType.Assistant &&
                            sendLoading &&
                            derivedMessages?.length - 1 === i
                          }
                          index={i}
                          clickDocumentButton={clickDocumentButton}
                          showLikeButton={false}
                          showLoudspeaker={false}
                        ></MessageItem>
                      )}
                    {!Object.hasOwn(data, 'showSuggestType') && (
                      <MessageItem
                        visibleAvatar={visibleAvatar}
                        avatarDialog={avatarData?.avatar}
                        item={message}
                        nickname="You"
                        reference={buildMessageItemReference(
                          {
                            message: derivedMessages,
                            reference: [],
                          },
                          message,
                        )}
                        loading={
                          message.role === MessageType.Assistant &&
                          sendLoading &&
                          derivedMessages?.length - 1 === i
                        }
                        index={i}
                        clickDocumentButton={clickDocumentButton}
                        showLikeButton={false}
                        showLoudspeaker={false}
                      ></MessageItem>
                    )}
                    {i === 0 &&
                      data &&
                      Object.hasOwn(data, 'showSuggestType') && (
                        <div
                          style={{ borderRadius: '10px', background: 'white' }}
                        >
                          <div className="relative">
                            {/* 背景块 */}
                            <div
                              style={{ borderBottom: '1px solid #e8e8e8' }}
                              className="bg-[url('@/assets/neu/banner.png')] flex justify-center items-center bg-cover rounded-[10px] m-w-[351px] h-[80px] mt-3"
                            >
                              {/* 头像 */}
                              <div className="absolute left-[18px] -top-2 w-[86px] h-[88px] bg-[url('@/assets/neu/mindle-age-woman.png')] bg-cover" />
                              {/* 文本内容 */}
                              <div className="text-center ml-8">
                                <div className="text-[12px] text-gray-600">
                                  Hi，我是您的数字健康人
                                </div>
                                <div className="text-[14px] font-bold text-gray-900">
                                  您可以试着向我提这些问题
                                </div>
                              </div>
                            </div>

                            {/* 问题列表 */}
                            {suggestedQuestions.map((question, index) => (
                              <div
                                key={index}
                                onClick={() =>
                                  handleSuggestedQuestionClick(question)
                                }
                                className="flex justify-between items-center h-[40px]"
                                style={{
                                  cursor: 'pointer',
                                  padding: '8px 16px',
                                  color: '#1890ff',
                                }}
                              >
                                <Text>{question}</Text>
                                <RightOutlined style={{ color: '#000000' }} />
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                  </div>
                );
              })}
            </Spin>
          </div>
          <div ref={ref} />
        </Flex>

        <MessageInput
          isShared
          value={value}
          disabled={hasError}
          sendDisabled={sendDisabled}
          conversationId={conversationId}
          onInputChange={handleInputChange}
          onPressEnter={handlePressEnter}
          sendLoading={sendLoading}
          uploadMethod="external_upload_and_parse"
          showUploadIcon={false}
          stopOutputMessage={stopOutputMessage}
        ></MessageInput>
      </Flex>
      {visible && (
        <PdfDrawer
          visible={visible}
          hideModal={hideModal}
          documentId={documentId}
          chunk={selectedChunk}
        ></PdfDrawer>
      )}
    </>
  );
};

export default forwardRef(ChatContainer);
