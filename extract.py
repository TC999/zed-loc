import re
import json
import os

# 注：只能在 Windows 系统运行！
# 定义文件路径列表
input_file_paths = [
    # 使用正斜杠路径确保跨平台兼容性
    # 文件读取规则，读代码时可跳过，如果词条缺失自行添加文件路径
    # activity_indicator
    r'zed\crates\activity_indicator\src\activity_indicator.rs',
    # agent gpt 面板
    r'zed\crates\agent\src\agent_panel.rs',
    # anthropic
    r'zed\crates\anthropic\src\anthropic.rs',
    # r'zed\crates\anthropic\src\supported_countries.rs',
    r'zed\crates\assets\src\assets.rs',
    # assistant 助手
    r'zed\crates\assistant\src\assistant_configuration.rs',
    r'zed\crates\assistant\src\assistant_panel.rs',
    #r'zed\crates\assistant\src\assistant_settings.rs',
    r'zed\crates\assistant\src\context_store.rs',
    r'zed\crates\assistant\src\context.rs',
    r'zed\crates\assistant\src\inline_assistant.rs',
    r'zed\crates\assistant\src\patch.rs',
    r'zed\crates\assistant\src\prompt_library.rs',
    r'zed\crates\assistant\src\slash_command_picker.rs',
    r'zed\crates\assistant\src\slash_command.rs',
    r'zed\crates\assistant\src\terminal_inline_assistant.rs',
    r'zed\crates\assistant_context_editor\src\context_editor.rs',
    # assistant_slash_command(s)
    #r'zed\crates\assistant_slash_command\src\assistant_slash_command.rs',
    r'zed\crates\assistant_slash_commands\src\diagnostics_command.rs',
    r'zed\crates\assistant_slash_commands\src\terminal_command.rs',
    # assistant_tools
    r'zed\crates\assistant_tools\src\now_tool.rs',
    # assistant2
    r'zed\crates\assistant2\src\active_thread.rs',
    r'zed\crates\assistant2\src\assistant_model_selector.rs',
    r'zed\crates\assistant2\src\assistant_panel.rs',
    r'zed\crates\assistant2\src\buffer_codegen.rs',
    r'zed\crates\assistant2\src\context_store.rs',
    r'zed\crates\assistant2\src\context_strip.rs',
    r'zed\crates\assistant2\src\context.rs',
    r'zed\crates\assistant2\src\inline_assistant.rs',
    r'zed\crates\assistant2\src\inline_prompt_editor.rs',
    r'zed\crates\assistant2\src\message_editor.rs',
    r'zed\crates\assistant2\src\terminal_inline_assistant.rs',
    r'zed\crates\assistant2\src\thread_history.rs',
    r'zed\crates\assistant2\src\thread_store.rs',
    r'zed\crates\assistant2\src\thread.rs',
    r'zed\crates\assistant2\src\context_picker\directory_context_picker.rs',
    r'zed\crates\assistant2\src\context_picker\fetch_context_picker.rs',
    r'zed\crates\assistant2\src\context_picker\file_context_picker.rs',
    r'zed\crates\assistant2\src\context_picker\thread_context_picker.rs',
    r'zed\crates\assistant2\src\ui\context_pill.rs',
    # audio
    r'zed\crates\audio\src\assets.rs',
    # auto_update
    r'zed\crates\auto_update\src\auto_update.rs',
    # auto_update_ui
    r'zed\crates\auto_update_ui\src\update_notification.rs',
    # breadcrumbs
    r'zed\crates\breadcrumbs\src\breadcrumbs.rs',
    # call
    r'zed\crates\call\src\cross_platform\mod.rs',
    r'zed\crates\call\src\cross_platform\participant.rs',
    r'zed\crates\call\src\cross_platform\room.rs',
    r'zed\crates\call\src\macos\mod.rs',
    r'zed\crates\call\src\macos\participant.rs',
    r'zed\crates\call\src\macos\room.rs',
    # channel
    r'zed\crates\channel\src\channel_buffer.rs',
    r'zed\crates\channel\src\channel_chat.rs',
    r'zed\crates\channel\src\channel_store.rs',
    # cli
    r'zed\crates\cli\src\main.rs',
    # client
    r'zed\crates\client\src\client.rs',
    r'zed\crates\client\src\socks.rs',
    r'zed\crates\client\src\telemetry.rs',
    r'zed\crates\client\src\test.rs',
    r'zed\crates\client\src\user.rs',
    # clock
    r'zed\crates\clock\src\clock.rs',
    # command_palette_hooks
    r'zed\crates\command_palette_hooks\src\command_palette_hooks.rs',
    # coolab
    r'zed\crates\collab\src\api\billing.rs',
    r'zed\crates\collab\src\api\contributors.rs',
    r'zed\crates\collab\src\api\events.rs',
    r'zed\crates\collab\src\api\extensions.rs',
    r'zed\crates\collab\src\api\ips_file.rs',
    r'zed\crates\collab\src\bin\dotenv.rs',
    r'zed\crates\collab\src\db\queries\access_tokens.rs',
    r'zed\crates\collab\src\db\queries\billing_preferences.rs',
    r'zed\crates\collab\src\db\queries\buffers.rs',
    r'zed\crates\collab\src\db\queries\channels.rs',
    r'zed\crates\collab\src\db\queries\contacts.rs',
    r'zed\crates\collab\src\db\queries\extensions.rs',
    r'zed\crates\collab\src\db\queries\messages.rs',
    r'zed\crates\collab\src\db\queries\notifications.rs',
    r'zed\crates\collab\src\db\queries\projects.rs',
    r'zed\crates\collab\src\db\queries\rooms.rs',
    r'zed\crates\collab\src\db\queries\users.rs',
    # coolab_ui
    r'zed\crates\collab_ui\src\chat_panel\message_editor.rs',
    r'zed\crates\collab_ui\src\collab_panel\channel_modal.rs',
    r'zed\crates\collab_ui\src\collab_panel\contact_finder.rs',
    r'zed\crates\collab_ui\src\notifications\stories\collab_notification.rs',
    r'zed\crates\collab_ui\src\notifications\incoming_call_notification.rs',
    r'zed\crates\collab_ui\src\notifications\project_shared_notification.rs',
    r'zed\crates\collab_ui\src\channel_view.rs',
    r'zed\crates\collab_ui\src\chat_panel.rs',
    r'zed\crates\collab_ui\src\collab_panel.rs',
    r'zed\crates\collab_ui\src\collab_ui.rs',
    r'zed\crates\collab_ui\src\notification_panel.rs',
    # command_palette
    r'zed\crates\command_palette\src\command_palette.rs',
    # copilot
    r'zed\crates\copilot\src\copilot_chat.rs',
    r'zed\crates\copilot\src\copilot.rs',
    r'zed\crates\copilot\src\sign_in.rs',
    # db
    r'zed\crates\db\src\db.rs',
    r'zed\crates\db\src\query.rs',
    # diagnostics
    r'zed\crates\diagnostics\src\diagnostics_tests.rs',
    r'zed\crates\diagnostics\src\diagnostics.rs',
    r'zed\crates\diagnostics\src\items.rs',
    r'zed\crates\diagnostics\src\toolbar_controls.rs',
    # docs_preprocessor
    r'zed\crates\docs_preprocessor\src\main.rs',
    # editor
    r'zed\crates\editor\src\git\blame.rs',
    r'zed\crates\editor\src\git\project_diff.rs',
    r'zed\crates\editor\src\blame_entry_tooltip.rs',
    r'zed\crates\editor\src\clangd_ext.rs',
    r'zed\crates\editor\src\code_context_menus.rs',
    r'zed\crates\editor\src\display_map.rs',
    r'zed\crates\editor\src\editor_settings_controls.rs',
    r'zed\crates\editor\src\editor_tests.rs',
    r'zed\crates\editor\src\editor.rs',
    r'zed\crates\editor\src\element.rs',
    r'zed\crates\editor\src\git.rs',
    r'zed\crates\editor\src\hover_links.rs',
    r'zed\crates\editor\src\hover_popover.rs',
    r'zed\crates\editor\src\hunk_diff.rs',
    r'zed\crates\editor\src\indent_guides.rs',
    r'zed\crates\editor\src\inlay_hint_cache.rs',
    r'zed\crates\editor\src\inline_completion_tests.rs',
    r'zed\crates\editor\src\items.rs',
    r'zed\crates\editor\src\linked_editing_ranges.rs',
    r'zed\crates\editor\src\lsp_ext.rs',
    r'zed\crates\editor\src\mouse_context_menu.rs',
    r'zed\crates\editor\src\movement.rs',
    r'zed\crates\editor\src\persistence.rs',
    r'zed\crates\editor\src\proposed_changes_editor.rs',
    r'zed\crates\editor\src\rust_analyzer_ext.rs',
    # extensions 扩展
    r'zed\crates\extension\src\extension_builder.rs',
    r'zed\crates\extension\src\extension_host_proxy.rs',
    r'zed\crates\extension\src\extension_manifest.rs',
    r'zed\crates\extension\src\extension.rs',
    r'zed\crates\extension\src\types.rs',
    # extension_api
    r'zed\crates\extension_api\src\extension_api.rs',
    r'zed\crates\extension_api\src\http_client.rs',
    r'zed\crates\extension_api\src\settings.rs',
    # extension_cli
    r'zed\crates\extension_cli\src\main.rs',
    # extensions_ui 扩展UI
    r'zed\crates\extensions_ui\src\components\extension_card.rs',
    r'zed\crates\extensions_ui\src\components\feature_upsell.rs',
    r'zed\crates\extensions_ui\src\extension_suggest.rs',
    r'zed\crates\extensions_ui\src\extension_version_selector.rs',
    r'zed\crates\extensions_ui\src\extensions_ui.rs',
    # feedback 反馈
    r'zed\crates\feedback\src\feedback_modal.rs',
    r'zed\crates\feedback\src\feedback.rs',
    r'zed\crates\feedback\src\system_specs.rs',
    # file_finder
    r'zed\crates\file_finder\src\file_finder_tests.rs',
    r'zed\crates\file_finder\src\file_finder.rs',
    r'zed\crates\file_finder\src\new_path_prompt.rs',
    r'zed\crates\file_finder\src\open_path_prompt.rs',
    # fireworks
    r'zed\crates\fireworks\src\fireworks.rs',
    # fsevent
    r'zed\crates\fsevent\examples\events.rs',
    r'zed\crates\fsevent\src\fsevent.rs',
    # fuzzy
    r'zed\crates\fuzzy\src\strings.rs',
    # git
    r'zed\crates\git\src\blame.rs',
    r'zed\crates\git\src\commit.rs',
    r'zed\crates\git\src\diff.rs',
    r'zed\crates\git\src\git.rs',
    r'zed\crates\git\src\remote.rs',
    r'zed\crates\git\src\repository.rs',
    r'zed\crates\git\src\status.rs',
    # git_hosting_providers
    r'zed\crates\git_hosting_providers\src\providers\codeberg.rs',
    r'zed\crates\git_hosting_providers\src\providers\github.rs',
    r'zed\crates\git_hosting_providers\src\providers\gitlab.rs',
    # git_ui
    r'zed\crates\git_ui\src\branch_picker.rs',
    r'zed\crates\git_ui\src\git_panel.rs',
    r'zed\crates\git_ui\src\git_ui.rs',
    r'zed\crates\git_ui\src\project_diff.rs',
    r'zed\crates\git_ui\src\remote_output.rs',
    # go_to_line
    r'zed\crates\go_to_line\src\cursor_position.rs',
    r'zed\crates\go_to_line\src\go_to_line.rs',
    # google_ai
    r'zed\crates\google_ai\src\google_ai.rs',
    # gpui
    r'zed\crates\gpui\examples\hello_world.rs',
    r'zed\crates\gpui\examples\image\image.rs',
    r'zed\crates\gpui\examples\set_menus.rs',
    r'zed\crates\gpui\examples\uniform_list.rs',
    r'zed\crates\gpui\examples\window_positioning.rs',
    r'zed\crates\gpui\src\elements\animation.rs',
    r'zed\crates\gpui\src\elements\div.rs',
    r'zed\crates\gpui\src\action.rs',
    r'zed\crates\gpui\src\app.rs',
    r'zed\crates\gpui\src\arena.rs',
    r'zed\crates\gpui\src\asset_cache.rs',
    r'zed\crates\gpui\src\color.rs',
    r'zed\crates\gpui\src\element.rs',
    r'zed\crates\gpui\src\executor.rs',
    r'zed\crates\gpui\src\key_dispatch.rs',
    #r'zed\crates\gpui\src\keymap.rs',
    r'zed\crates\gpui\src\platform\linux\platform.rs',
    r'zed\crates\gpui\src\platform\windows\platform.rs',
    # html_to_markdown
    r'zed\crates\html_to_markdown\src\html_to_markdown.rs',
    r'zed\crates\html_to_markdown\src\markdown_writer.rs',
    # http_client
    r'zed\crates\http_client\src\github.rs',
    r'zed\crates\http_client\src\http_client.rs',
    # image_viewer
    r'zed\crates\image_viewer\src\image_viewer.rs',
    # indexed_docs
    r'zed\crates\indexed_docs\src\providers\rustdoc.rs',
    r'zed\crates\indexed_docs\src\store.rs',
    # inline_completion_button
    r'zed\crates\inline_completion_button\src\inline_completion_button.rs',
    # install_cli
    r'zed\crates\install_cli\src\install_cli.rs',
    # language
    r'zed\crates\language\src\buffer_tests.rs',
    # language_model_selector
    r'zed\crates\language_model_selector\src\language_model_selector.rs',
    # language_selector
    r'zed\crates\language_selector\src\active_buffer_language.rs',
    r'zed\crates\language_selector\src\language_selector.rs',
    # language_models
    r'zed\crates\language_models\src\provider\anthropic.rs',
    r'zed\crates\language_models\src\provider\bedrock.rs',
    r'zed\crates\language_models\src\provider\cloud.rs',
    r'zed\crates\language_models\src\provider\copilot_chat.rs',
    r'zed\crates\language_models\src\provider\deepseek.rs',
    r'zed\crates\language_models\src\provider\google.rs',
    r'zed\crates\language_models\src\provider\lmstudio.rs',
    r'zed\crates\language_models\src\provider\mistral.rs',
    r'zed\crates\language_models\src\provider\ollama.rs',
    r'zed\crates\language_models\src\provider\open_ai.rs',
    r'zed\crates\language_models\src\logging.rs',
    # markdown
    r'zed\crates\markdown\examples\markdown.rs',
    # media 媒体
    r'zed\crates\media\src\media.rs',
    r'zed\crates\media\build.rs',
    # node_runtime
    r'zed\crates\node_runtime\src\node_runtime.rs',
    # notifications 通知
    r'zed\crates\notifications\src\notification_store.rs',
    # ollama
    r'zed\crates\ollama\src\ollama.rs',
    # open_ai
    r'zed\crates\open_ai\src\open_ai.rs',
    # outline 大纲
    r'zed\crates\outline\src\outline.rs',
    # outline_panel 大纲面板
    r'zed\crates\outline_panel\src\outline_panel.rs',
    # paths 路径
    r'zed\crates\paths\src\paths.rs',
    # prettier
    r'zed\crates\prettier\src\prettier.rs',
    # project
    r'zed\crates\project\src\buffer_store.rs',
    r'zed\crates\project\src\color_extractor.rs',
    r'zed\crates\project\src\direnv.rs',
    r'zed\crates\project\src\environment.rs',
    r'zed\crates\project\src\image_store.rs',
    r'zed\crates\project\src\lsp_command.rs',
    r'zed\crates\project\src\lsp_store.rs',
    r'zed\crates\project\src\prettier_store.rs',
    r'zed\crates\project\src\project_settings.rs',
    r'zed\crates\project\src\project.rs',
    r'zed\crates\project\src\search_history.rs',
    r'zed\crates\project\src\search.rs',
    r'zed\crates\project\src\task_inventory.rs',
    r'zed\crates\project\src\task_store.rs',
    r'zed\crates\project\src\terminals.rs',
    r'zed\crates\project\src\toolchain_store.rs',
    r'zed\crates\project\src\worktree_store.rs',
    # project_panel
    r'zed\crates\project_panel\src\project_panel.rs',
    # prompt_library
    r'zed\crates\prompt_library\src\prompt_library.rs',
    r'zed\crates\prompt_library\src\prompt_store.rs',
    r'zed\crates\prompt_library\src\prompts.rs',
    # recent_projects
    r'zed\crates\recent_projects\src\disconnected_overlay.rs',
    r'zed\crates\recent_projects\src\recent_projects.rs',
    r'zed\crates\recent_projects\src\remote_servers.rs',
    r'zed\crates\recent_projects\src\ssh_connections.rs',
    # refineable
    r'zed\crates\refineable\derive_refineable\src\derive_refineable.rs',
    # repl
    r'zed\crates\repl\src\components\kernel_options.rs',
    r'zed\crates\repl\src\kernels\native_kernel.rs',
    r'zed\crates\repl\src\kernels\remote_kernels.rs',
    r'zed\crates\repl\src\notebook\notebook_ui.rs',
    r'zed\crates\repl\src\outputs\image.rs',
    r'zed\crates\repl\src\outputs.rs',
    r'zed\crates\repl\src\repl_editor.rs',
    r'zed\crates\repl\src\repl_sessions_ui.rs',
    r'zed\crates\repl\src\repl_store.rs',
    r'zed\crates\repl\src\session.rs',
    # request_client
    r'zed\crates\reqwest_client\src\reqwest_client.rs',
    # rope
    r'zed\crates\rope\src\chunk.rs',
    # rpc
    r'zed\crates\rpc\src\auth.rs',
    r'zed\crates\rpc\src\peer.rs',
    r'zed\crates\rpc\src\proto_client.rs',
    # search 搜索
    r'zed\crates\search\src\buffer_search.rs',
    r'zed\crates\search\src\mode.rs',
    r'zed\crates\search\src\project_search.rs',
    r'zed\crates\search\src\search.rs',
    # semantic_index
    r'zed\crates\semantic_index\examples\index.rs',
    r'zed\crates\semantic_index\src\embedding\cloud.rs',
    r'zed\crates\semantic_index\src\embedding\ollama.rs',
    r'zed\crates\semantic_index\src\chunking.rs',
    r'zed\crates\semantic_index\src\embedding_index.rs',
    r'zed\crates\semantic_index\src\embedding.rs',
    r'zed\crates\semantic_index\src\project_index_debug_view.rs',
    r'zed\crates\semantic_index\src\project_index.rs',
    r'zed\crates\semantic_index\src\semantic_index.rs',
    r'zed\crates\semantic_index\src\worktree_index.rs',
    # semantic_version
    r'zed\crates\semantic_version\src\semantic_version.rs',
    # settings 设置
    r'zed\crates\settings\src\keymap_file.rs',
    r'zed\crates\settings\src\settings_file.rs',
    r'zed\crates\settings\src\settings_store.rs',
    # settings_ui 设置UI
    #r'zed\crates\settings_ui\src\appearance_settings_controls.rs',
    #r'zed\crates\settings_ui\src\settings_ui.rs',
    r'zed\crates\settings_ui\src\page_data.rs',
    # snippet
    r'zed\crates\snippet\src\snippet.rs',
    # snippet_ui
    r'zed\crates\snippets_ui\src\snippets_ui.rs',
    # sqlez
    r'zed\crates\sqlez\src\bindable.rs',
    r'zed\crates\sqlez\src\connection.rs',
    r'zed\crates\sqlez\src\migrations.rs',
    r'zed\crates\sqlez\src\savepoint.rs',
    r'zed\crates\sqlez\src\statement.rs',
    r'zed\crates\sqlez\src\thread_safe_connection.rs',
    r'zed\crates\sqlez\src\typed_statements.rs',
    # streaming_diff
    r'zed\crates\streaming_diff\src\streaming_diff.rs',
    # tab_switcher
    r'zed\crates\tab_switcher\src\tab_switcher.rs',
    # task
    r'zed\crates\task\src\task_template.rs',
    r'zed\crates\task\src\vscode_format.rs',
    # tasks_ui
    r'zed\crates\tasks_ui\src\modal.rs',
    # terminal 终端
    r'zed\crates\terminal\src\terminal.rs',
    # terminal_view
    r'zed\crates\terminal_view\src\persistence.rs',
    r'zed\crates\terminal_view\src\terminal_panel.rs',
    r'zed\crates\terminal_view\src\terminal_tab_tooltip.rs',
    r'zed\crates\terminal_view\src\terminal_view.rs',
    # text 文本
    r'zed\crates\text\src\text.rs',
    # theme_importer
    r'zed\crates\theme_importer\src\assets.rs',
    r'zed\crates\theme_importer\src\main.rs',
    # theme_selector 主题选择器
    r'zed\crates\theme_selector\src\theme_selector.rs',
    r'zed\crates\theme_selector\src\icon_theme_selector.rs',
    # time_format 时间格式
    r'zed\crates\time_format\src\time_format.rs',
    # title_bar 标题栏
    r'zed\crates\title_bar\src\application_menu.rs',
    r'zed\crates\title_bar\src\collab.rs',
    r'zed\crates\title_bar\src\title_bar.rs',
    r'zed\crates\title_bar\src\window_controls.rs',
    # toolchain_selector 工具链选择器
    r'zed\crates\toolchain_selector\src\active_toolchain.rs',
    r'zed\crates\toolchain_selector\src\toolchain_selector.rs',
    # util
    r'zed\crates\util\src\paths.rs',
    r'zed\crates\util\src\test.rs',
    r'zed\crates\util\src\util.rs',
    # vcs_menu
    r'zed\crates\vcs_menu\src\lib.rs',
    # vim
    r'zed\crates\vim\src\change_list.rs',
    r'zed\crates\vim\src\mode_indicator.rs',
    r'zed\crates\vim\src\normal.rs',
    r'zed\crates\vim\src\surrounds.rs',
    # welcome 欢迎
    r'zed\crates\welcome\src\base_keymap_picker.rs',
    r'zed\crates\welcome\src\multibuffer_hint.rs',
    r'zed\crates\welcome\src\welcome.rs',
    # workspace 工作区
    r'zed\crates\workspace\src\notifications.rs',
    r'zed\crates\workspace\src\pane_group.rs',
    r'zed\crates\workspace\src\pane.rs',
    r'zed\crates\workspace\src\persistence.rs',
    r'zed\crates\workspace\src\theme_preview.rs',
    r'zed\crates\workspace\src\workspace.rs',
    r'zed\crates\worktree\src\worktree.rs',
    # worktree 工作树
    r'zed\crates\worktree\src\worktree_settings.rs',
    # zed
    r'zed\crates\zed\src\main.rs',
    r'zed\crates\zed\src\reliability.rs',
    r'zed\crates\zed\src\zed.rs',
    r'zed\crates\zed\src\zed\app_menus.rs',
    r'zed\crates\zed\src\zed\mac_only_instance.rs',
    r'zed\crates\zed\src\zed\open_listener.rs',
    r'zed\crates\zed\src\zed\quick_action_bar.rs',
    r'zed\crates\zed\src\zed\windows_only_instance.rs',
    r'zed\crates\zed\src\zed\quick_action_bar\markdown_preview.rs',
    r'zed\crates\zed\src\zed\quick_action_bar\repl_menu.rs',
    # zeta
    r'zed\crates\zeta\src\zeta.rs',
]
output_file_path = 'string.json'

# 初始化JSON数据
json_data = {}

# 遍历每个文件路径
for input_file_path in input_file_paths:
    
    # 读取文件内容
    if os.name != 'nt':  # 只非Windows系统下替换反斜杠
        input_file_path = input_file_path.replace('\\', '/')
    if not os.path.exists(input_file_path):
        print(f"File not found: {input_file_path}, skipping.")
        continue

    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式查找所有引号中的字符串，考虑转义引号的情况
    pattern = r'"((?:\\.|[^"\\])*)"'
    matches = re.findall(pattern, content)

    # 构建JSON数据
    json_data[os.path.normpath(input_file_path).replace('\\', '/')] = {match: "" for match in matches}

# 将JSON数据写入文件
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)

print(f'Successfully extracted strings to {output_file_path}')
