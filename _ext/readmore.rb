module Awestruct
  module Extensions
    module ReadMore
      def truncate(content)
        index = content.index("pass::[more]")
        if index != nil && index > -1
          # check for additional opened and unclosed <p> tag
          if (content[index-3..index-1].casecmp "<p>") == 0
            return content[0..index-4]
          else
            return content[0..index-1]
          end
        end
        return content
      end
      def filter(content)
        index = content.index("pass::[more]")
        if index != nil && index > -1
                content[index..index+11]= ''
        end
        content
      end
    end
  end
end

